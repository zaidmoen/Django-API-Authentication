# Django API Authentication

**A structured Django REST API backend with MySQL and JWT authentication.**

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.16%2B-A30000)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?logo=mysql&logoColor=white)

## Overview

This project is a clean Django REST API foundation for applications that need user authentication and protected resources. It includes registration, JWT login and refresh, user-specific task management, ownership permissions, request tracing, structured logging, signals, Django Admin, and a custom management command.

## Features

- JWT authentication with access and refresh tokens
- Secure user registration with Django password hashing
- Authenticated `Task` CRUD API
- Task priorities, categories and due dates
- Task filtering, search and pagination
- Object-level ownership permissions
- Custom request logging middleware
- Unique `X-Request-ID` header and execution-time tracking
- Logging to the terminal and `django.log`
- `post_save` signal for new users
- JSON validation decorator for write requests
- Django Admin integration
- Demo data command: `python manage.py seed_demo`
- MySQL configuration through environment variables
- Automated API tests

## Architecture

```text
Client → Middleware → URL Router → View/ViewSet → Serializer → Model → MySQL
```

## Project Structure

```text
config/
├── settings.py       # Django, MySQL, REST framework and logging configuration
├── urls.py            # Root URL configuration and JWT routes
└── wsgi.py            # WSGI entry point

api/
├── models.py          # Task database model
├── serializers.py     # JSON validation and representation
├── views.py           # Registration, profile and task endpoints
├── permissions.py     # Owner-only access policy
├── middleware.py      # Request IDs, timing and request logs
├── signals.py         # User creation event handling
├── decorators.py      # JSON content-type validation
└── management/        # Custom Django commands
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create the database:

```sql
CREATE DATABASE django_api_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copy `.env.example` to `.env` and configure your MySQL password:

```env
MYSQL_DATABASE=django_api_db
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Apply migrations and run the server:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## API Reference

| Method | Endpoint | Auth | Purpose |
|---|---|---:|---|
| `GET` | `/` | No | API status response |
| `POST` | `/api/auth/register/` | No | Register a user |
| `POST` | `/api/auth/token/` | No | Obtain JWT tokens |
| `POST` | `/api/auth/token/refresh/` | No | Refresh an access token |
| `GET` | `/api/auth/me/` | Yes | Get current user |
| `GET` / `POST` | `/api/tasks/` | Yes | List or create tasks |
| `GET` / `PATCH` / `DELETE` | `/api/tasks/{id}/` | Yes | Manage one own task |
| `GET` | `/api/tasks/completed/` | Yes | List completed tasks |

Task list filters can be combined:

```text
GET /api/tasks/?status=todo&priority=high&category=study&search=exam&page=1&page_size=10
```

Available task fields are `title`, `description`, `status`, `priority`, `category`,
and `due_date`. Priority values are `low`, `medium`, and `high`. The list endpoint
returns paginated results with `count`, `next`, `previous`, and `results` fields.

### Authentication

Send credentials to `/api/auth/token/`:

```json
{
  "username": "zaid",
  "password": "StrongPass123!"
}
```

Use the returned access token on protected requests:

```text
Authorization: Bearer <access-token>
```

More examples are available in [`docs/API_EXAMPLES.md`](docs/API_EXAMPLES.md).

## Useful Commands

```powershell
python manage.py test
python manage.py check
python manage.py seed_demo
python manage.py runserver
```

## Security Notes

- Never commit `.env` or production secrets.
- Use a strong `DJANGO_SECRET_KEY` in production.
- Set `DJANGO_DEBUG=False` in production.
- Restrict `DJANGO_ALLOWED_HOSTS` to trusted domains.
- Serve the API over HTTPS in production.

## License

This project is available under the MIT License.
