# Gym Backend Starter

This project is a starter FastAPI backend for a gym application.

## Features

- User registration
- User login with JWT token
- Weekly workout plan API
- SQLite database for easy local setup

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
- `GET /workouts/weekly`
- `GET /workouts/days/{day_name}`

## Example weekly split

- Monday: Legs
- Tuesday: Chest
- Wednesday: Lats
- Thursday: Shoulders
- Friday: Back + Legs
- Saturday: Hands
- Sunday: Active Rest

## Free deployment options

GitHub alone does not run a FastAPI backend. Use GitHub for code hosting, then deploy for free on:

- Render
- Koyeb
- Railway (limited free options depending on current plan)

If you want, I can guide you next to deploy this step by step.
