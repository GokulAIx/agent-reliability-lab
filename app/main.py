"""Minimal FastAPI entry point for an agent run."""

import os
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from solari_browser import Solari

from .agent import BrowserAgent

app = FastAPI(title="Agent Reliability Lab")


class RunRequest(BaseModel):
    task: str


@app.post("/runs")
async def create_run(request: RunRequest) -> dict[str, object]:
    api_key = os.environ.get("SOLARI_API_KEY")
    demo_url = os.environ.get("DEMO_URL")
    if not api_key or not demo_url or not os.environ.get("GOOGLE_API_KEY"):
        raise HTTPException(status_code=500, detail="Server agent configuration is incomplete")
    if not urlparse(demo_url).scheme:
        demo_url = f"https://{demo_url}"
    try:
        async with Solari(api_key=api_key) as solari:
            async with await solari.launch() as browser:
                page = await browser.new_page()
                await page.goto(demo_url, wait_until="domcontentloaded")
                result = await BrowserAgent(
                    page,
                    model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
                    max_steps=int(os.environ.get("MAX_STEPS", "12")),
                ).run(request.task)
                return {
                    "status": result.status,
                    "message": result.message,
                    "claimed_success": result.claimed_success,
                    "steps": result.actions,
                }
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Agent run failed: {error}") from error