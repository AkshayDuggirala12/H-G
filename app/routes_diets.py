from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, UserPlanAssignment
from app.schemas import DietPlanResponse


router = APIRouter(prefix="/diets", tags=["Diet Plans"])


@router.get("/my-plan", response_model=DietPlanResponse)
def get_my_diet_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if not assignment or not assignment.diet_plan:
        raise HTTPException(status_code=404, detail="No diet plan assigned for this user")
    return assignment.diet_plan
