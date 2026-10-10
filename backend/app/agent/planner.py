"""The planner decides which tool (if any) the LLM wants to call next.
It does not execute anything — that is the executor's job."""
from app.agent.llm import OllamaClient


class Planner:
    def __init__(self, llm: OllamaClient | None = None):
        self.llm = llm or OllamaClient()

    async def decide(self, messages: list[dict], tool_defs: list[dict]) -> dict:
        """Ask the LLM. Returns the assistant message dict with optional 'tool_calls'."""
        return await self.llm.chat(messages, tools=tool_defs)