from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, UserExerciseProgress, UserPlanAssignment, WorkoutPlanDay, WorkoutPlanExercise
from app.schemas import (
    ExerciseProgressStatus,
    ExerciseProgressToggle,
    WeeklyProgressItem,
    WorkoutDayProgressResponse,
)


router = APIRouter(prefix="/progress", tags=["Progress"])


def get_assigned_workout_plan_day(
    db: Session,
    current_user: User,
    day_name: str,
) -> WorkoutPlanDay:
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if not assignment or not assignment.workout_plan:
        raise HTTPException(status_code=404, detail="No workout plan assigned for this user")

    workout_day = (
        db.query(WorkoutPlanDay)
        .filter(
            WorkoutPlanDay.workout_plan_id == assignment.workout_plan_id,
            WorkoutPlanDay.day_name == day_name.strip().lower(),
        )
        .first()
    )
    if not workout_day:
        raise HTTPException(status_code=404, detail="Workout day not found in assigned plan")
    return workout_day


def get_assigned_workout_day_from_exercise(
    db: Session,
    current_user: User,
    exercise_id: int,
) -> tuple[WorkoutPlanDay, WorkoutPlanExercise]:
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if not assignment or not assignment.workout_plan:
        raise HTTPException(status_code=404, detail="No workout plan assigned for this user")

    exercise = (
        db.query(WorkoutPlanExercise)
        .join(WorkoutPlanDay, WorkoutPlanExercise.workout_day_id == WorkoutPlanDay.id)
        .filter(
            WorkoutPlanExercise.id == exercise_id,
            WorkoutPlanDay.workout_plan_id == assignment.workout_plan_id,
        )
        .first()
    )
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found in assigned workout plan")
    return exercise.workout_day, exercise


def build_day_progress(workout_day: WorkoutPlanDay, progress_date: date, user_id: int) -> WorkoutDayProgressResponse:
    progress_map = {
        progress.exercise_id: progress
        for progress in workout_day.progress_entries
        if progress.user_id == user_id and progress.progress_date == progress_date
    }

    exercise_statuses = [
        ExerciseProgressStatus(
            exercise_id=exercise.id,
            exercise_name=exercise.name,
            is_completed=bool(progress_map.get(exercise.id) and progress_map[exercise.id].is_completed),
            completed_at=progress_map.get(exercise.id).completed_at if progress_map.get(exercise.id) else None,
            gif_url=exercise.gif_url,
            instructions=exercise.instructions,
        )
        for exercise in workout_day.exercises
    ]

    total_exercises = len(exercise_statuses)
    completed_exercises = sum(1 for exercise in exercise_statuses if exercise.is_completed)
    remaining_exercises = max(total_exercises - completed_exercises, 0)
    percentage = round((completed_exercises / total_exercises) * 100, 2) if total_exercises else 0.0

    return WorkoutDayProgressResponse(
        day_name=workout_day.day_name,
        title=workout_day.title,
        progress_date=progress_date,
        completed_exercises=completed_exercises,
        total_exercises=total_exercises,
        remaining_exercises=remaining_exercises,
        percentage=percentage,
        is_day_completed=total_exercises > 0 and completed_exercises == total_exercises,
        exercises=exercise_statuses,
    )


@router.post("/exercise/toggle", response_model=WorkoutDayProgressResponse)
def toggle_exercise_progress(
    payload: ExerciseProgressToggle,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    progress_date = payload.progress_date or date.today()
    workout_day, target_exercise = get_assigned_workout_day_from_exercise(db, current_user, payload.exercise_id)

    progress = (
        db.query(UserExerciseProgress)
        .filter(
            UserExerciseProgress.user_id == current_user.id,
            UserExerciseProgress.exercise_id == target_exercise.id,
            UserExerciseProgress.progress_date == progress_date,
        )
        .first()
    )

    if not progress:
        progress = UserExerciseProgress(
            user_id=current_user.id,
            workout_day_id=workout_day.id,
            exercise_id=target_exercise.id,
            progress_date=progress_date,
        )
        db.add(progress)

    progress.is_completed = payload.is_completed
    progress.completed_at = datetime.now(timezone.utc) if payload.is_completed else None
    db.commit()

    refreshed_day = db.query(WorkoutPlanDay).filter(WorkoutPlanDay.id == workout_day.id).first()
    return build_day_progress(refreshed_day, progress_date, current_user.id)


@router.get("/days/{day_name}", response_model=WorkoutDayProgressResponse)
def get_day_progress(
    day_name: str,
    progress_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_day = get_assigned_workout_plan_day(db, current_user, day_name)
    return build_day_progress(workout_day, progress_date or date.today(), current_user.id)


@router.get("/weekly", response_model=list[WeeklyProgressItem])
def get_weekly_progress(
    progress_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.query(UserPlanAssignment).filter(UserPlanAssignment.user_id == current_user.id).first()
    if not assignment or not assignment.workout_plan:
        raise HTTPException(status_code=404, detail="No workout plan assigned for this user")

    selected_date = progress_date or date.today()
    workout_days = (
        db.query(WorkoutPlanDay)
        .filter(WorkoutPlanDay.workout_plan_id == assignment.workout_plan_id)
        .order_by(WorkoutPlanDay.sort_order.asc(), WorkoutPlanDay.id.asc())
        .all()
    )

    weekly_items: list[WeeklyProgressItem] = []
    for workout_day in workout_days:
        day_progress = build_day_progress(workout_day, selected_date, current_user.id)
        weekly_items.append(
            WeeklyProgressItem(
                day_name=workout_day.day_name,
                title=workout_day.title,
                progress_date=selected_date,
                completed_exercises=day_progress.completed_exercises,
                total_exercises=day_progress.total_exercises,
                remaining_exercises=day_progress.remaining_exercises,
                percentage=day_progress.percentage,
                is_day_completed=day_progress.is_day_completed,
            )
        )

    return weekly_items
