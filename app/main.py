from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.routes_auth import router as auth_router
from app.routes_workouts import router as workouts_router
from app.seed import seed_workouts


Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_workouts(db)


app = FastAPI(title="Gym App API", version="1.0.0")

app.include_router(auth_router)
app.include_router(workouts_router)


@app.get("/")
def root():
    return {"message": "Gym App API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
