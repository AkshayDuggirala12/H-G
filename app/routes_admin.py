from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin_user
from app.models import (
    ClientAccessRequest,
    DietMeal,
    DietPlan,
    User,
    UserPlanAssignment,
    WorkoutPlan,
    WorkoutPlanDay,
    WorkoutPlanExercise,
)
from app.schemas import (
    DietPlanCreate,
    DietPlanResponse,
    UserPlanAssignmentRequest,
    UserPlanAssignmentResponse,
    UserResponse,
    UserSummaryResponse,
    WorkoutPlanCreate,
    WorkoutPlanResponse,
)


router = APIRouter(prefix="/admin", tags=["Admin"])


def build_assignment_response(assignment: UserPlanAssignment) -> UserPlanAssignmentResponse:
    return UserPlanAssignmentResponse(
        user=UserResponse.model_validate(assignment.user),
        workout_plan=WorkoutPlanResponse.model_validate(assignment.workout_plan) if assignment.workout_plan else None,
        diet_plan=DietPlanResponse.model_validate(assignment.diet_plan) if assignment.diet_plan else None,
        assigned_at=assignment.assigned_at,
    )


@router.get("/users", response_model=list[UserSummaryResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    users = db.query(User).order_by(User.id.asc()).all()
    return [
        UserSummaryResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            workout_plan_id=user.plan_assignment.workout_plan_id if user.plan_assignment else None,
            diet_plan_id=user.plan_assignment.diet_plan_id if user.plan_assignment else None,
        )
        for user in users
    ]


@router.post("/workout-plans", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def create_workout_plan(
    payload: WorkoutPlanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    existing_plan = db.query(WorkoutPlan).filter(WorkoutPlan.name == payload.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Workout plan name already exists")

    workout_plan = WorkoutPlan(name=payload.name, description=payload.description)
    db.add(workout_plan)
    db.flush()

    for index, day in enumerate(payload.days):
        workout_day = WorkoutPlanDay(
            workout_plan_id=workout_plan.id,
            day_name=day.day_name.strip().lower(),
            title=day.title,
            description=day.description,
            video_url=day.video_url,
            sort_order=index,
        )
        db.add(workout_day)
        db.flush()

        for exercise in day.exercises:
            db.add(
                WorkoutPlanExercise(
                    workout_day_id=workout_day.id,
                    name=exercise.name,
                    sets=exercise.sets,
                    reps=exercise.reps,
                )
            )

    db.commit()
    return db.query(WorkoutPlan).filter(WorkoutPlan.id == workout_plan.id).first()


@router.get("/workout-plans", response_model=list[WorkoutPlanResponse])
def list_workout_plans(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return db.query(WorkoutPlan).order_by(WorkoutPlan.id.asc()).all()


@router.post("/diet-plans", response_model=DietPlanResponse, status_code=status.HTTP_201_CREATED)
def create_diet_plan(
    payload: DietPlanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    existing_plan = db.query(DietPlan).filter(DietPlan.name == payload.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Diet plan name already exists")

    diet_plan = DietPlan(name=payload.name, description=payload.description)
    db.add(diet_plan)
    db.flush()

    for meal in payload.meals:
        db.add(
            DietMeal(
                diet_plan_id=diet_plan.id,
                meal_name=meal.meal_name,
                meal_time=meal.meal_time,
                foods=meal.foods,
                notes=meal.notes,
            )
        )

    db.commit()
    return db.query(DietPlan).filter(DietPlan.id == diet_plan.id).first()


@router.get("/diet-plans", response_model=list[DietPlanResponse])
def list_diet_plans(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return db.query(DietPlan).order_by(DietPlan.id.asc()).all()


@router.post("/users/{user_id}/assign-plans", response_model=UserPlanAssignmentResponse)
def assign_plans_to_user(
    user_id: int,
    payload: UserPlanAssignmentRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workout_plan = None
    if payload.workout_plan_id is not None:
        workout_plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == payload.workout_plan_id).first()
        if not workout_plan:
            raise HTTPException(status_code=404, detail="Workout plan not found")

    diet_plan = None
    if payload.diet_plan_id is not None:
        diet_plan = db.query(DietPlan).filter(DietPlan.id == payload.diet_plan_id).first()
        if not diet_plan:
            raise HTTPException(status_code=404, detail="Diet plan not found")

    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == user.id).first()
    if not assignment:
        assignment = UserPlanAssignment(user_id=user.id)
        db.add(assignment)

    assignment.workout_plan_id = payload.workout_plan_id
    assignment.diet_plan_id = payload.diet_plan_id
    assignment.assigned_at = datetime.now(timezone.utc)

    latest_pending_request = (
        db.query(ClientAccessRequest)
        .filter(
            ClientAccessRequest.user_id == user.id,
            ClientAccessRequest.status == "pending",
        )
        .order_by(ClientAccessRequest.created_at.desc(), ClientAccessRequest.id.desc())
        .first()
    )
    if latest_pending_request and (payload.workout_plan_id is not None or payload.diet_plan_id is not None):
        latest_pending_request.status = "approved"

    db.commit()
    refreshed_assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == user.id).first()
    return build_assignment_response(refreshed_assignment)
