"""Deterministic browser failures used by reliability experiments."""

from typing import Any, Awaitable, Callable

from patchright.async_api import Page

EventHandler = Callable[[dict[str, Any]], Awaitable[None] | None]


async def inject_ui_mutation(page: Page, on_event: EventHandler | None = None) -> None:
    """Rename the primary cart action without changing application state."""
    await page.evaluate(
        """() => {
            const button = document.querySelector('#add-to-cart');
            if (!button) throw new Error('primary cart button was not found');
            button.textContent = 'Add to basket';
            button.setAttribute('aria-label', 'Add to basket');
        }"""
    )
    if on_event is not None:
        outcome = on_event({"type": "chaos_injected", "data": {"scenario": "ui_mutation"}})
        if outcome is not None:
            await outcome