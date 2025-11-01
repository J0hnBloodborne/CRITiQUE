CRITiQUE server (prototype)

Python/Flask server (prototype)

Install (recommended: use a virtualenv):
  cd server
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1   # in PowerShell; or use activate on other shells
  pip install -r requirements.txt

Run:
  python app.py

Server will listen on http://localhost:5000

API endpoints (prototype):
- POST /api/auth/register { email, name, university, password }
- POST /api/auth/login { email }
- GET /api/places
- POST /api/places { name, type, address, photo, tags }
- GET /api/places/:id
- POST /api/places/:id/reviews { userId, rating, text }
- PUT /api/reviews/:id { userId, rating?, text? }
- DELETE /api/reviews/:id { userId }
- GET /api/analytics

Realtime: Socket.io emits newReview, updateReview, deleteReview. Clients should connect to ws://localhost:5000 (Socket.IO client). 

Notes:
- Database: SQLite file 'campuseats.db' is created in the server folder. For production, migrate to PostgreSQL or MongoDB.
- This is a prototype with mocked auth. Replace with hashed passwords and JWTs or SSO for production.
