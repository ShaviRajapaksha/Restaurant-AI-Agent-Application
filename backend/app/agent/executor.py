from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Any
from sqlalchemy.orm import Session

from app.agent.tools.registry import registry
from app.core.database import SessionLocal


class ToolExecutor:
    def __init__(self, db, user_id: int):
        # db may be sync (from a request) or async (from the SSE stream).
        # Tools run on a *fresh sync session* so they don't touch the async session.
        self.db = db
        self.user_id = user_id

    # --- used by sync callers ---
    def execute(self, name: str, arguments: dict) -> dict[str, Any]:
        tool = registry.get(name)
        if not tool:
            return {"error": f"Unknown tool '{name}'"}
        args = dict(arguments or {})
        sig_args = tool.handler.__code__.co_varnames[: tool.handler.__code__.co_argcount]
        if "user_id" in sig_args:
            args["user_id"] = self.user_id
        args["db"] = self.db
        try:
            result = tool.handler(**args)
            return result if isinstance(result, (dict, list)) else {"result": result}
        except TypeError as exc:
            return {"error": f"Invalid arguments for tool '{name}': {exc}"}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc)}

    # --- used by the async agent runtime ---
    async def execute_async(self, name: str, arguments: dict) -> dict[str, Any]:
        return await asyncio.to_thread(self._execute_with_fresh_session, name, arguments)

    def _execute_with_fresh_session(self, name: str, arguments: dict) -> dict[str, Any]:
        db = SessionLocal()  # brand-new sync session, thread-local
        try:
            executor = ToolExecutor(db, self.user_id)
            return executor.execute(name, arguments)
        finally:
            db.close()