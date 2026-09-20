# Contributing

Thank you for helping improve this project.

## Scope

This project is for endpoint telemetry on devices explicitly enrolled by their owner or administrator.

Contributions must not add password, cookie, authentication-token, session, keystroke, clipboard, camera, microphone, private-message, or arbitrary personal-file collection. Do not add covert persistence, evasion, or unenrolled-device collection.

## Development

Use Python 3.12+ and a virtual environment.

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements-agent.txt
python -m pip install -r requirements-server.txt
python -m pip install pytest pytest-asyncio ruff mypy
python -m pytest -q
ruff check .
```

## Pull requests

Keep changes focused, explain security/privacy impact, add tests for behavior changes, and update documentation when commands or configuration change.

Never commit secrets, telemetry databases, device credentials, private keys, or generated build output.
