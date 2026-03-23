from fastapi import FastAPI

from app.database import SessionLocal, initialize_database
from app.routes_admin import router as admin_router
from app.routes_auth import router as auth_router
from app.routes_diets import router as diets_router
from app.routes_progress import router as progress_router
from app.routes_workouts import router as workouts_router
from app.seed import seed_default_plans


initialize_database()

with SessionLocal() as db:
    seed_default_plans(db)


app = FastAPI(title="Gym App API", version="1.0.0")

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(diets_router)
app.include_router(progress_router)
app.include_router(workouts_router)


@app.get("/")
def root():
    return {"message": "Gym App API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
