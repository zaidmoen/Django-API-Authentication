# API Examples

## Register

```http
POST /api/auth/register/
Content-Type: application/json
```

```json
{
  "username": "zaid",
  "email": "zaid@example.com",
  "password": "StrongPass123!"
}
```

## Obtain JWT

```http
POST /api/auth/token/
Content-Type: application/json
```

```json
{
  "username": "zaid",
  "password": "StrongPass123!"
}
```

Use the returned access token as:

```http
Authorization: Bearer <access-token>
```

## Create a task

```http
POST /api/tasks/
Content-Type: application/json
Authorization: Bearer <access-token>
```

```json
{
  "title": "Practice Django",
  "description": "Review middleware, signals and logging.",
  "status": "todo"
}
```

