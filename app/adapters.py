"""Agent adapter boundary owned by the reliability lab."""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Protocol

from patchright.async_api import Page

from .agent import BrowserAgent
from .models import AgentResult

EventHandler = Callable[[dict[str, Any]], Awaitable[None] | None]


class AgentAdapter(Protocol):
    """Contract for any agent that the lab can test inside a browser session."""

    async def run(self, task: str, page: Page, emit: EventHandler | None = None) -> AgentResult:
        ...


class LangGraphReferenceAdapter:
    """The contest demo agent; the lab remains independent of its framework."""

    def __init__(self, *, model: str, max_steps: int) -> None:
        self.model = model
        self.max_steps = max_steps

    async def run(self, task: str, page: Page, emit: EventHandler | None = None) -> AgentResult:
        return await BrowserAgent(
            page,
            model=self.model,
            max_steps=self.max_steps,
            on_event=emit,
        ).run(task)