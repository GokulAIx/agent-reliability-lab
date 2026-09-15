# Agent Reliability Lab

Agent Reliability Lab is a reliability and chaos-testing harness for browser-based AI agents running inside Solari.

## Phase 1

Phase 1 proves the smallest end-to-end path:

```text
Python -> Solari -> cloud browser -> public demo -> Playwright interaction -> cleanup
```

The demo is a static site in `demo/`. Deploy that directory as a Vercel project and set its public URL in `DEMO_URL`.

## Run the smoke test

Requirements: Python 3.11+ and a Solari API key.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the environment variables in the current PowerShell session:

```powershell
$env:SOLARI_API_KEY = "slr_live_..."
$env:DEMO_URL = "https://your-demo.vercel.app"
python -m app.smoke
```

## Run the LLM agent

Once the updated demo is deployed, run the Gemini/LangGraph browser agent:

```powershell
.venv\Scripts\Activate.ps1
python -m app.run_demo
```

The agent receives the natural-language task, observes the page, chooses browser tools, and iterates until it claims success or reaches `MAX_STEPS`. The independent verifier remains a separate component and is not used by the agent to decide whether it succeeded.

## Run an experiment

Run the baseline:

```powershell
.venv\Scripts\python.exe -m app.experiment
```

Run the first controlled UI mutation:

```powershell
$env:CHAOS_SCENARIO = "ui_mutation"
.venv\Scripts\python.exe -m app.experiment
```

Run a one-time network failure against the cart request:

```powershell
$env:CHAOS_SCENARIO = "network_failure"
.venv\Scripts\python.exe -m app.experiment
```

Expire the session before the agent acts:

```powershell
$env:CHAOS_SCENARIO = "session_expiration"
.venv\Scripts\python.exe -m app.experiment
```

The report compares the agent claim with independent application state and classifies the run as `SUCCESS`, `RECOVERED`, `FAILURE`, `FALSE SUCCESS`, or `UNCERTAIN`.

The experiment runner targets the `AgentAdapter` contract. The included Gemini/LangGraph implementation is the reference adapter used by the demo; the reliability layer is designed to test other agents through the same boundary.

Experiment reports can be persisted in SQLite by setting `RUN_DB_PATH` (the FastAPI experiment endpoint defaults to `data/runs.db`). The stored report includes the classification, agent claim, verifier result, and event evidence.

To run the FastAPI entry point:

```powershell
uvicorn app.main:app --reload
```

Then post a task to `POST /runs` with JSON such as:

```json
{"task":"Find the cheapest laptop under ₹80,000 and add it to the cart."}
```

Expected output:

```text
page: Solari Demo Store
interaction: ThinkPad X1 added to cart
cleanup: browser session released
```

The API key stays server-side. Do not put it in the demo site or commit a populated `.env` file.

## Deploy the demo to Vercel

Create a Vercel project whose root directory is `demo/`, or deploy the directory directly with the Vercel CLI:

```powershell
vercel demo
```

Copy the resulting public URL into `DEMO_URL`. The cloud browser must be able to reach this URL; a local `localhost` URL will not work.