"""
Restaurant Agent Runtime.

A genuine agent loop:
  1. Feed conversation + state + tools to the LLM.
  2. If the LLM requests a tool, execute it via ToolExecutor.
  3. Append the tool result to the transcript.
  4. Loop until the LLM produces a final natural-language answer (or max steps reached).
  5. If a tool requires confirmation and the user hasn't confirmed, block the call and ask.

Events emitted to the frontend: "status", "tool_call", "tool_result", "message".
"""
import json
from typing import AsyncIterator, Any
from datetime import date
from sqlalchemy.orm import Session

from app.agent.llm import OllamaClient
from app.agent.planner import Planner
from app.agent.executor import ToolExecutor
from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import register_all_tools, registry
from app.models.chat import MessageRole
from app.repositories.chat_repo import ConversationRepository


CONFIRMATION_WORDS = {"yes", "y", "confirm", "book it", "go ahead", "please do", "ok", "okay", "sure"}


class AgentRuntime:
    def __init__(self, db: Session, user_id: int, conversation_id: int):
        register_all_tools()
        self.db = db
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.chat_repo = ConversationRepository(db)
        self.planner = Planner(OllamaClient())
        self.executor = ToolExecutor(db, user_id)

    # ---------- helpers ----------

    def _build_messages(self, state: AgentState, prior_messages: list) -> list[dict]:
        messages: list[dict] = [
            {"role": "system", "content": SYSTEM_PROMPT + f"\nToday: {date.today().isoformat()}"},
            {"role": "system", "content": f"Current agent state JSON:\n{json.dumps(state.to_dict(), default=str)}"},
        ]
        for m in prior_messages[-30:]:
            role = m.role.value.lower()
            if role == "system":
                continue
            if role == "tool":
                continue  # tool messages are not exposed to the LLM directly
            messages.append({"role": role, "content": m.content or ""})
        return messages

    def _user_confirmed_last_turn(self, prior_messages: list) -> bool:
        # Look at the last user message
        for m in reversed(prior_messages):
            if m.role == MessageRole.USER:
                txt = (m.content or "").strip().lower()
                return txt in CONFIRMATION_WORDS or any(txt.startswith(w + " ") for w in CONFIRMATION_WORDS)
        return False

    def _extract_state_updates(self, user_message: str, state: AgentState) -> None:
        """Very lightweight heuristic state extraction to support multi-turn memory.
        The LLM handles nuanced parsing; this ensures we don't lose simple facts
        (party size, cuisine, city, budget) between turns."""
        import re
        text = user_message.lower()

        m = re.search(r"(\d+)\s*(people|persons|guests|pax)", text)
        if m:
            state.party_size = int(m.group(1))

        m = re.search(r"under\s*(?:rs\.?|lkr)?\s*([\d,]+)", text)
        if m:
            state.budget = int(m.group(1).replace(",", ""))

        for cuisine in ["italian", "chinese", "japanese", "indian", "sri lankan", "mexican", "thai", "american"]:
            if cuisine in text:
                state.cuisine = cuisine.title()
                break

        for city in ["colombo", "kandy", "galle", "negombo", "jaffna"]:
            if city in text:
                state.location = city.title()
                break

        m = re.search(r"\b(\d{1,2}):(\d{2})\s*(am|pm)?", text)
        if m:
            hh, mm, ampm = m.group(1), m.group(2), m.group(3)
            state.time = f"{hh}:{mm}"
        elif "7 pm" in text or "7pm" in text:
            state.time = "19:00"

    # ---------- main loop ----------

    async def run(self, user_message: str) -> AsyncIterator[dict]:
        """Runs the agent loop; yields event dicts. Persists messages as side-effects."""

        # 1. persist user message
        self.chat_repo.add_message(self.conversation_id, MessageRole.USER, user_message)
        self.db.commit()

        # 2. load state
        conv = self.chat_repo.get(self.conversation_id)
        state = AgentState.from_dict(conv.agent_state or {})
        self._extract_state_updates(user_message, state)

        # 3. gather prior messages (now includes the new user message)
        prior = self.chat_repo.get_messages(self.conversation_id)
        confirmed = self._user_confirmed_last_turn(prior[:-1] if prior else [])

        messages = self._build_messages(state, prior)
        tool_defs = registry.ollama_definitions()

        final_text = ""
        max_steps = 6

        for step in range(max_steps):
            yield {"type": "status", "data": {"message": "Thinking..."}}

            try:
                assistant_msg = await self.planner.decide(messages, tool_defs)
            except Exception as exc:  # noqa: BLE001
                yield {"type": "error", "data": {"message": f"LLM error: {exc}"}}
                return

            tool_calls = assistant_msg.get("tool_calls") or []
            content = assistant_msg.get("content") or ""

            if not tool_calls:
                final_text = content or "I'm not sure how to help with that yet."
                break

            # Handle the (typically single) tool call
            for tc in tool_calls:
                fn = tc.get("function", {})
                name = fn.get("name")
                raw_args = fn.get("arguments") or {}
                if isinstance(raw_args, str):
                    try:
                        raw_args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        raw_args = {}

                tool = registry.get(name)

                # Confirmation gate
                if tool and tool.requires_confirmation and not confirmed:
                    # Block and ask user to confirm
                    summary = self._describe_pending(state, name, raw_args)
                    state.pending_confirmation = {"tool": name, "arguments": raw_args}
                    self.chat_repo.save_state(conv, state.to_dict())
                    self.chat_repo.add_message(self.conversation_id, MessageRole.ASSISTANT, summary,
                                               payload={"requires_confirmation": True, **state.pending_confirmation})
                    self.db.commit()
                    yield {"type": "status", "data": {"message": "Waiting for confirmation"}}
                    yield {"type": "message", "data": {"content": summary,
                                                        "requires_confirmation": True,
                                                        "pending": state.pending_confirmation}}
                    return

                yield {"type": "tool_call", "data": {"name": name, "arguments": raw_args}}
                result = self.executor.execute(name, raw_args)

                # log
                self.chat_repo.log_tool(self.conversation_id, name, raw_args, result,
                                        error=result.get("error") if isinstance(result, dict) else None)
                self.db.commit()

                yield {"type": "tool_result", "data": {"name": name, "result": result}}

                # feed tool result back to LLM
                messages.append({
                    "role": "assistant",
                    "content": content,
                    "tool_calls": tool_calls,
                })
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result, default=str),
                    "name": name,
                })

                # update state based on the tool
                self._apply_tool_to_state(name, raw_args, result, state)

                # clear pending after successful confirmation-protected execution
                if tool and tool.requires_confirmation:
                    state.pending_confirmation = None

        if not final_text:
            final_text = "I ran into a limit processing that request. Could you rephrase?"

        # persist assistant
        payload = self._build_payload_from_state(state)
        self.chat_repo.add_message(self.conversation_id, MessageRole.ASSISTANT, final_text, payload=payload)
        self.chat_repo.save_state(conv, state.to_dict())
        self.db.commit()

        yield {"type": "message", "data": {"content": final_text, "payload": payload}}

    # ---------- state helpers ----------

    def _apply_tool_to_state(self, name: str, args: dict, result: dict, state: AgentState) -> None:
        if name == "search_restaurants" and isinstance(result, dict):
            state.last_search_results = result.get("restaurants", [])
        elif name == "get_restaurant_menu" and isinstance(result, dict):
            state.selected_restaurant_id = result.get("restaurant_id")
            state.selected_restaurant_name = result.get("restaurant_name")
        elif name == "create_reservation" and isinstance(result, dict):
            state.reservation_id = result.get("reservation_id")
            state.selected_restaurant_id = result.get("restaurant_id")
        elif name == "create_order" and isinstance(result, dict):
            state.order_id = result.get("order_id")

    def _build_payload_from_state(self, state: AgentState) -> dict | None:
        payload: dict[str, Any] = {}
        if state.last_search_results:
            payload["restaurants"] = state.last_search_results
        if state.selected_restaurant_id:
            payload["selected_restaurant_id"] = state.selected_restaurant_id
        if state.reservation_id:
            payload["reservation_id"] = state.reservation_id
        if state.order_id:
            payload["order_id"] = state.order_id
        return payload or None

    def _describe_pending(self, state: AgentState, name: str, args: dict) -> str:
        if name == "create_reservation":
            rid = args.get("restaurant_id") or state.selected_restaurant_id
            name_ = state.selected_restaurant_name or f"restaurant #{rid}"
            return (
                f"Just to confirm — I'll book {name_} for "
                f"{args.get('party_size', state.party_size)} people on "
                f"{args.get('date', state.date)} at {args.get('time', state.time)}. "
                "Shall I go ahead?"
            )
        if name == "create_order":
            return "Shall I place this order now?"
        if name == "cancel_reservation":
            return f"Shall I cancel reservation #{args.get('reservation_id')}?"
        return "Shall I proceed?"