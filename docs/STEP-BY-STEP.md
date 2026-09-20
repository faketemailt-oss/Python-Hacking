# Step-by-Step Implementation & Usage Guide

This guide is the project's **waterfall implementation path**. Complete one step, verify it, then move to the next. Do not skip ahead.

> Scope: this project is for explicitly enrolled devices and collects only non-sensitive endpoint telemetry. It does not collect passwords, cookies, tokens, private messages, keystrokes, clipboard contents, camera/microphone data, or arbitrary personal files.

## Waterfall rule

For every step:

1. Read the goal.
2. Perform only that step.
3. Run the listed verification command.
4. Confirm the expected result.
5. Only then continue.

## Step 0 — Understand the architecture

**Goal:** Know what you are building before installing anything.

Components:

- **Agent:** runs on an enrolled device and collects approved telemetry.
- **Collectors:** small modules that collect specific non-sensitive categories.
- **Local database/queue:** stores telemetry until it can be delivered.
- **Server:** receives authenticated reports and manages enrollment/revocation.
- **Telegram reporter:** optional server-side reporting; secrets never belong in the agent or Git.
- **Tests/CI:** verify the project continuously.

Expected result: you can explain the difference between the agent and server.

---

## Step 1 — Prepare Windows

**Goal:** Verify Python and Git.

PowerShell:

```powershell
py --version
git --version
```

Expected result:

- Python 3.12 or newer.
- Git is installed.

If Python is missing, install Python 3.12+ before continuing.

---

## Step 2 — Clone the repository

**Goal:** Put the project on your PC.

```powershell
git clone https://github.com/faketemailt-oss/Python-Hacking.git
cd Python-Hacking
```

Verify:

```powershell
git status
```

Expected result: Git reports the `main` branch and a clean working tree.

---

## Step 3 — Create the Python virtual environment

**Goal:** Keep project dependencies isolated.

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python --version
```

Expected result: the prompt shows `.venv` and Python reports 3.12+.

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\\.venv\\Scripts\\Activate.ps1
```

This changes policy only for the current PowerShell process.

---

## Step 4 — Install dependencies

**Goal:** Install the libraries required by the agent, server, tests, and tooling.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-agent.txt
python -m pip install -r requirements-server.txt
python -m pip install pytest pytest-asyncio ruff mypy
```

Verify:

```powershell
python -c "import fastapi, httpx, psutil, cryptography; print('Dependencies OK')"
```

Expected result:

```text
Dependencies OK
```

---

## Step 5 — Create local configuration

**Goal:** Create local settings without putting secrets in Git.

Copy the example:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

Never commit a real token, password, private key, or device credential.

Verify Git ignores it:

```powershell
git status --short
```

Expected result: `.env` does not appear as an untracked file.

---

## Step 6 — Run the automated tests

**Goal:** Establish a known-good baseline before changing configuration.

```powershell
python -m pytest -q
```

Then:

```powershell
ruff check .
```

Expected result: tests pass and Ruff reports no errors.

If this step fails, stop here and fix the failure before continuing.

---

## Step 7 — Run the server locally

**Goal:** Start the management/reporting API on your own PC.

```powershell
python -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

Keep this terminal open.

In a second PowerShell window:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

Expected result: the server returns a successful health response.

Stop the server with `Ctrl+C`.

---

## Step 8 — Run a local telemetry collection

**Goal:** Confirm the agent can collect the approved telemetry categories locally.

With the virtual environment active:

```powershell
python -m agent.main --collect-once
```

Expected result:

- The process exits normally.
- Local telemetry is generated.
- No passwords, browser cookies, private messages, keystrokes, clipboard data, camera/microphone data, or arbitrary files are collected.

---

## Step 9 — Understand enrollment before enrolling a device

**Goal:** Make sure reporting is authorized.

The intended flow is:

```text
Administrator
    |
    | creates/controls enrollment
    v
Server enrollment endpoint
    |
    | issues device credential
    v
Explicitly enrolled device
    |
    | authenticated telemetry
    v
Server
```

A device must not report merely because the agent is installed.

Expected result: you understand that installation and enrollment are separate operations.

---

## Step 10 — Enroll a test device

**Goal:** Enroll only a device you own or administer.

Use the server's enrollment workflow documented by the current implementation.

Record:

- device ID
- enrollment state
- enabled telemetry categories
- server URL
- credential storage location

Do not paste credentials into GitHub, README files, screenshots, or chat.

Expected result: the device state is **ENROLLED** and the server recognizes the device.

---

## Step 11 — Send an authenticated report

**Goal:** Verify the complete agent-to-server path.

Start the server, then run the agent's report operation using the enrolled configuration.

Verify on the server:

- device identity is recognized
- authentication succeeds
- telemetry is accepted
- invalid/revoked credentials are rejected

Expected result: an authorized device can report and an unauthorized/revoked device cannot.

---

## Step 12 — Test offline queue and resume

**Goal:** Verify reliability when the server is temporarily unavailable.

1. Stop the server.
2. Run a collection/report operation.
3. Confirm telemetry remains in the local queue.
4. Start the server again.
5. Run the delivery operation.
6. Confirm queued telemetry is delivered.

Expected result: telemetry is not silently lost just because the server was temporarily unavailable.

---

## Step 13 — Test revocation

**Goal:** Verify immediate access removal.

1. Enroll a test device.
2. Confirm it can report.
3. Revoke that device on the server.
4. Attempt another report.

Expected result: the server rejects the revoked device.

---

## Step 14 — Configure Telegram reporting (optional)

**Goal:** Send server-side reports to an authorized Telegram destination.

Telegram is optional. The bot token belongs only on the server.

Set environment variables on the server:

```text
TELEGRAM_BOT_TOKEN=<real token>
TELEGRAM_CHAT_ID=<authorized chat id>
```

Do not place these values in:

- Git
- `.env.example`
- source code
- screenshots
- README
- the agent configuration

Expected result: the server can generate a readable report without exposing the bot token.

---

## Step 15 — Build the Windows EXE

**Goal:** Package the agent for normal Windows deployment to explicitly enrolled devices.

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Build:

```powershell
pyinstaller --name Python-Hacking-Agent --onedir agent/main.py
```

The generated application will be under `dist\\`.

Before distribution:

- test it on a clean test machine
- enroll the machine explicitly
- verify collection and reporting
- verify revocation
- review Windows security warnings
- sign the executable for production distribution

---

## Step 16 — Daily development workflow

Before making changes:

```powershell
git pull
```

After changes:

```powershell
python -m pytest -q
ruff check .
git status
```

Then commit:

```powershell
git add .
git commit -m "Describe the change"
git push origin main
```

Never commit:

- `.env`
- databases containing telemetry
- device credentials
- private keys
- exported telemetry
- local session files
- build output

---

## Step 17 — Production checklist

Before real deployment:

- [ ] Every device is explicitly enrolled.
- [ ] Collection categories are documented.
- [ ] Server uses HTTPS.
- [ ] Device credentials can be revoked.
- [ ] Local queue has bounded storage.
- [ ] Server database has backups and retention controls.
- [ ] Telegram secrets are server-side only.
- [ ] Logs do not contain credentials or sensitive payloads.
- [ ] Windows EXE is tested and signed.
- [ ] CI is passing.
- [ ] Privacy/security documentation is available to device owners/admins.

## Troubleshooting order

When something fails, do not change five things at once.

Use this order:

1. `python --version`
2. virtual environment active
3. dependencies installed
4. `.env` configured locally
5. tests passing
6. server health endpoint
7. enrollment state
8. authentication
9. local queue
10. Telegram reporting

Fix the first failing layer, test again, then continue.

## Recommended learning sequence

For a beginner, use this exact order:

**Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7 → Step 8 → Step 9 → Step 10 → Step 11 → Step 12 → Step 13 → Step 14 → Step 15 → Step 16 → Step 17**

Do not jump directly to the EXE or Telegram integration before the local tests and enrollment flow work.
