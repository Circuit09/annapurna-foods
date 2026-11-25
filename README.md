# Annapurna Foods

The public homepage is available at `/`. The internal business manager is at `/manager`.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000/manager. The SQLite database is created as `annapurna.db` on first start; it is local business data and must not be committed.
