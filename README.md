# Python-Hacking — Consent-Based Endpoint Telemetry

A structured, beginner-friendly Python project for collecting **non-sensitive system telemetry from explicitly enrolled devices** and optionally forwarding reports to a private server and Telegram.

## What this project does

- Collects operating-system and hardware inventory.
- Collects disk/storage usage.
- Collects installed-application metadata where supported.
- Detects installed browser executables without reading browser history, cookies, passwords, or sessions.
- Collects network-interface metadata such as interface state and IP addresses.
- Collects battery/power status when available.
- Stores unsent telemetry locally when the server is unavailable.
- Authenticates enrolled devices with server-issued credentials.
- Supports revocation at the server.
- Provides a FastAPI server and optional Telegram reporting helper.
- Includes automated tests and GitHub Actions CI.

## What it deliberately does NOT do

This is not a RAT, spyware, credential stealer, keylogger, or covert monitoring tool.

It does not collect:
- passwords or credentials
- browser cookies or authentication tokens
- Telegram/WhatsApp/private-message content
- keystrokes or clipboard contents
- webcam or microphone recordings
- arbitrary personal documents/files
- data from devices that have not been explicitly enrolled

## Repository layout

```text
Python-Hacking/
├── agent/                 # Endpoint agent
│   ├── collectors/        # Safe telemetry collectors
│   ├── security/          # Enrollment/local encryption helpers
│   ├── storage/           # Offline queue/database
│   ├── transport/         # HTTPS API client
│   ├── config.py
│   └── main.py
├── server/                # FastAPI management/reporting server
│   ├── enrollment/
│   ├── device_registry/
│   ├── reporting/
│   ├── database.py
│   ├── models.py
│   ├── security.py
│   └── main.py
├── android/               # Android implementation notes/limitations
├── tests/                 # Automated tests
├── .github/workflows/     # CI
├── .env.example           # Configuration template; no secrets
├── requirements-*.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## Requirements

- Python 3.12+
- Windows, Linux, or macOS for the desktop agent
- Internet access only when reports need to reach the server
- A Telegram bot is optional and is configured only on the server

## First-time setup

### 1. Clone

```powershell
git clone https://github.com/faketemailt-oss/Python-Hacking.git
cd Python-Hacking
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install agent dependencies

```powershell
python -m pip install -r requirements-agent.txt
```

### 4. Install server dependencies

```powershell
python -m pip install -r requirements-server.txt
```

### 5. Configure

Copy `.env.example` to `.env`.

Never put a real Telegram bot token, private key, password, or device credential into Git.

## Run the server

```powershell
uvicorn server.main:app --host 127.0.0.1 --port 8000
```

Health check:

```text
GET /health
```

## Enrollment model

Enrollment is explicit. The server has an administrator enrollment code. A device presents its generated device ID plus that administrator code to the enrollment endpoint. The server returns a device credential. The credential is then used for authenticated telemetry reports.

Revoke a device through the server-side device registry before allowing it to report again.

For production deployment, place the API behind HTTPS and protect administrator enrollment with an appropriate access-control layer.

## Telegram configuration

Telegram is optional and server-side only.

Set these environment variables on the server:

```text
TELEGRAM_BOT_TOKEN=<your real token>
TELEGRAM_CHAT_ID=<your authorized chat ID>
```

Do not commit either value.

The repository intentionally contains only empty configuration fields in `.env.example`.

## Run the agent

For a one-time local collection:

```powershell
python -m agent.main --collect-once
```

The agent creates its local data directory and queues telemetry locally when it has no enrolled transport credential or when the server cannot be reached.

## Testing

```powershell
python -m pytest -q
ruff check .
```

CI runs tests and Ruff on Python 3.12.

## Building a Windows EXE

Install PyInstaller in the virtual environment:

```powershell
python -m pip install pyinstaller
```

Then package the agent entry point:

```powershell
pyinstaller --name Python-Hacking-Agent --onedir agent/main.py
```

For a production release, use a reviewed PyInstaller spec and sign the resulting executable before distributing it to enrolled devices.

## Security and privacy

- Keep the server and database private.
- Use HTTPS outside localhost.
- Keep Telegram credentials server-side.
- Rotate/revoke device credentials when a device leaves the enrollment scope.
- Do not commit `.env`, databases, session files, private keys, or exports.
- Keep collection categories limited to the minimum required.
- Tell device owners/admins what is collected and why.

## Development policy

Changes should preserve the consent-based telemetry boundary. New collectors must document exactly which fields they collect and must not expand into credentials, private communications, keystrokes, clipboard data, surveillance media, or arbitrary file collection.

## Beginner step-by-step implementation

If you want to build and use this project one task at a time, follow the repository's **waterfall guide**. Complete each step, run its verification command, and only then continue.

**Guide:** [docs/STEP-BY-STEP.md](docs/STEP-BY-STEP.md)

The guide covers setup, virtual environment, dependencies, configuration, tests, server startup, local collection, enrollment, authenticated reporting, offline queue/resume, revocation, optional Telegram reporting, Windows EXE packaging, daily Git workflow, and production checks.

## License

MIT
