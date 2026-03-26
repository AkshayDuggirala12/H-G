from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin_user, get_current_user
from app.models import ClientAccessRequest, User, UserPlanAssignment
from app.notifications import send_access_request_notification
from app.schemas import (
    AssignedPlansResponse,
    ClientAccessRequestAdminResponse,
    ClientAccessRequestCreate,
    ClientAccessRequestResponse,
)


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/my-plans", response_model=AssignedPlansResponse)
def get_my_assigned_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if not assignment or (not assignment.workout_plan and not assignment.diet_plan):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workout or diet plan assigned for this user",
        )

    return AssignedPlansResponse(
        workout_plan=assignment.workout_plan,
        diet_plan=assignment.diet_plan,
    )


@router.post("/access-request", response_model=ClientAccessRequestResponse, status_code=status.HTTP_201_CREATED)
def create_access_request(
    payload: ClientAccessRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if assignment and (assignment.workout_plan_id or assignment.diet_plan_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plans already assigned for this user",
        )

    access_request = ClientAccessRequest(
        user_id=current_user.id,
        age=payload.age,
        weight_kg=payload.weight_kg,
        height_cm=payload.height_cm,
        workout_frequency=payload.workout_frequency,
        goals=payload.goals,
    )
    db.add(access_request)
    db.commit()
    db.refresh(access_request)

    try:
        send_access_request_notification(current_user, access_request)
    except Exception:
        pass

    return access_request


@router.get("/access-request/me", response_model=list[ClientAccessRequestResponse])
def list_my_access_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ClientAccessRequest)
        .filter(ClientAccessRequest.user_id == current_user.id)
        .order_by(ClientAccessRequest.created_at.desc())
        .all()
    )


@router.get("/access-requests", response_model=list[ClientAccessRequestAdminResponse])
def list_client_access_requests(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    requests = (
        db.query(ClientAccessRequest)
        .order_by(ClientAccessRequest.created_at.desc(), ClientAccessRequest.id.desc())
        .all()
    )
    return [
        ClientAccessRequestAdminResponse(
            id=request_item.id,
            status=request_item.status,
            age=request_item.age,
            weight_kg=request_item.weight_kg,
            height_cm=request_item.height_cm,
            workout_frequency=request_item.workout_frequency,
            goals=request_item.goals,
            created_at=request_item.created_at,
            user=request_item.user,
        )
        for request_item in requests
    ]
