# FleetIQ

Kubernetes fleet health & anomaly intelligence — a lightweight, self-hostable service
that collects health metrics from many clusters, stores the history, and (later) uses
ML/AI to surface anomalies and suggest fixes.

> Works on any Kubernetes: AKS, EKS, or a local `kind` cluster. No vendor lock-in.

## Status

Early development. Phase 0: core API.

## Quick start (local)

```bash
# create + activate a virtual environment (Windows PowerShell)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt

# run the API
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000/health — health check
- http://127.0.0.1:8000/docs — interactive API docs (auto-generated)

## License

MIT — free for companies to use and adapt in their own environments.
