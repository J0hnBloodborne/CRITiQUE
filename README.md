CRITiQUE — prototype

This is a minimal prototype for CRITiQUE: a student review platform.

Structure:
- server/  — Python Flask app (server-rendered templates, SQLite via SQLAlchemy). No client-side JavaScript.
- client/  — informational static page (not used for UI).

Quick start (server):
1. Install Python 3.10+ and create a virtualenv.
2. In PowerShell:
   ```powershell
   Set-Location 'd:\Code\CampusEats\server'
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```

Server runs by default on http://localhost:5000

Then open http://localhost:5000 in your browser to use the server-rendered UI (no JavaScript required).

Notes:
- The app uses SQLite (campuseats.db) for storage. For production, migrate to PostgreSQL or MongoDB.
- Auth is mocked (email-based login). Replace with proper password hashing and tokens / SSO for production.
