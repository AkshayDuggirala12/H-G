from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, UserPlanAssignment
from app.schemas import WorkoutPlanResponse


router = APIRouter(prefix="/workouts", tags=["Workouts"])


def get_user_assignment(db: Session, user_id: int) -> UserPlanAssignment | None:
    return db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == user_id).first()


@router.get("/my-plan", response_model=WorkoutPlanResponse)
def get_my_workout_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = get_user_assignment(db, current_user.id)
    if not assignment or not assignment.workout_plan:
        raise HTTPException(status_code=404, detail="No workout plan assigned for this user")
    return assignment.workout_plan
