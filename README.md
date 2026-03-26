# Gym Backend Starter

This project is a starter FastAPI backend for a gym application.

## Features

- User registration
- User login with JWT token
- Admin-created workout and diet plans
- Client plan assignment by user ID
- Workout progress tracking
- Client intake/access request flow
- SQLite or PostgreSQL support

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Main endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /admin/workout-plans`
- `POST /admin/diet-plans`
- `POST /admin/users/{user_id}/assign-plans`
- `GET /clients/my-plans`
- `POST /clients/access-request`
- `GET /clients/access-request/me`
- `GET /clients/access-requests`
- `GET /progress/weekly`
- `GET /progress/days/{day_name}`

## Trainer workflow

- Register/login as admin using the email set in `ADMIN_EMAIL`
- Create workout plans with `POST /admin/workout-plans`
- Create diet plans with `POST /admin/diet-plans`
- Assign both plans to a client with `POST /admin/users/{user_id}/assign-plans`
- Clients fetch their assigned plans with `GET /clients/my-plans`
- Unassigned clients can submit age, weight, height, workout frequency, and goals with `POST /clients/access-request`
- Admin can review requests with `GET /clients/access-requests`

## Free deployment options

GitHub alone does not run a FastAPI backend. Use GitHub for code hosting, then deploy for free on:

- Render
- Koyeb
- Railway (limited free options depending on current plan)

If you want, I can guide you next to deploy this step by step.
