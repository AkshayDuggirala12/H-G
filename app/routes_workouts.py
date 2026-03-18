from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import WorkoutDay
from app.schemas import WorkoutDayResponse


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/weekly", response_model=list[WorkoutDayResponse])
def get_weekly_workout_plan(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(WorkoutDay).order_by(WorkoutDay.id.asc()).all()


@router.get("/days/{day_name}", response_model=WorkoutDayResponse)
def get_workout_by_day(day_name: str, db: Session = Depends(get_db), _=Depends(get_current_user)):
    workout_day = (
        db.query(WorkoutDay)
        .filter(WorkoutDay.day_name == day_name.strip().lower())
        .first()
    )
    if not workout_day:
        raise HTTPException(status_code=404, detail="Workout day not found")
    return workout_day
