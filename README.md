# Python-Hacking

Consent-based endpoint telemetry for devices explicitly enrolled by their owners or administrators.

## Safety boundary

This project is defensive telemetry, not malware. It does not collect passwords, cookies, authentication/session tokens, private messages, keystrokes, clipboard contents, webcam/microphone data, arbitrary personal files, or data from unenrolled devices.

## Stack

Python 3.12+, asyncio, SQLite, psutil, FastAPI, httpx, cryptography, Pydantic, pytest, Ruff, mypy.

## Quick start

### Agent
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-agent.txt
python -m agent.main
```

### Server
```powershell
python -m pip install -r requirements-server.txt
uvicorn server.main:app --reload
```

Copy `.env.example` to `.env` and configure local values. Never commit real secrets.

## Telegram

The server optionally reports enrolled-device summaries through the Telegram Bot API. Configure `TELEGRAM_BOT_TOKEN` only in the server environment. It is intentionally absent from source control.

## Testing

```powershell
python -m pytest -q
ruff check .
mypy agent server
```

## License

MIT
