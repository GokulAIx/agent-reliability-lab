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