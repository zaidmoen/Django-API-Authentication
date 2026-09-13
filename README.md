# Django API Project

Simple Django + MySQL API with JWT authentication, tasks CRUD, custom middleware, logging, signals, decorators, admin, and a custom management command.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create the MySQL database first: `CREATE DATABASE django_api_db CHARACTER SET utf8mb4;`

## Endpoints

- `POST /api/auth/register/` with `username`, `email`, `password`
- `POST /api/auth/token/` with `username`, `password`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `GET/POST /api/tasks/`
- `GET/PUT/PATCH/DELETE /api/tasks/<id>/`
- `GET /api/tasks/completed/`

Send `Authorization: Bearer <access_token>` to protected endpoints.

Run demo seed: `python manage.py seed_demo`.

