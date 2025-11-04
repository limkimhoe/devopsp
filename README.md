
# python-postgresql

Minimal Flask example with PostgreSQL support.

Description
- Small Flask app located in `project_flask/`
- SQLAlchemy configured to use `DATABASE_URL` (falls back to `sqlite:///dev.db`)
- Dockerfile and `docker-compose.yml` provided to run the app with Postgres

Quickstart — Docker (recommended)
1. Ensure Docker and docker-compose are installed.
2. From repository root run:
   docker-compose up --build
3. The web service will be available at: http://localhost:8000
4. Postgres listens on port 5432 (host: localhost), credentials from docker-compose:
   - user: postgres
   - password: postgres
   - db: postgres

Local development (without Docker)
1. Create and activate a virtualenv:
   - Windows:
     python -m venv .venv
     .venv\Scripts\activate
   - macOS / Linux:
     python -m venv .venv
     source .venv/bin/activate
2. Install requirements:
   pip install -r requirements.txt
3. Optionally point the app to a running Postgres instance:
   - Windows (cmd): set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
   - PowerShell: $env:DATABASE_URL='postgresql://postgres:postgres@localhost:5432/postgres'
   - macOS / Linux: export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
4. Run the app for development:
   python project_flask/app.py
   (This will start Flask on 0.0.0.0:5000 by default.)

Notes
- The Dockerfile runs the app with gunicorn on port 8000; `docker-compose.yml` maps 8000:8000.
- Alembic is included in requirements for DB migrations; configure `alembic.ini` and `env.py` when adding migrations.
- The app provides a simple Example model in `project_flask/app.py` to verify DB connectivity.

Next steps
- Add migrations and an init script for the DB
- Add basic tests and CI configuration
- Harden production settings (secrets, connection pooling, fewer gunicorn workers, healthchecks)

# Run Flask Application
1 CPU
gunicorn --bind 0.0.0.0:8000 project_flask.app:app --workers 1 &

2 CPU
gunicorn --bind 0.0.0.0:8000 project_flask.app:app --workers 5 &

# Kill PID
for pid in /proc/[0-9]*; do
  cmdfile="$pid/cmdline"
  if [ -r "$cmdfile" ]; then
    cmd=$(tr '\0' ' ' < "$cmdfile" | sed -e 's/ $//')
    if echo "$cmd" | grep -E "project_flask.app:app|gunicorn|:8000" >/dev/null 2>&1; then
      echo "KILLING PID $(basename $pid): $cmd"
      kill -9 "$(basename $pid)" 2>/dev/null || true
    fi
  fi
done
sleep 1
curl -I http://127.0.0.1:8000 || true
