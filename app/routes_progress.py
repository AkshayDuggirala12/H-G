from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Exercise, ExerciseProgress, User, WorkoutDay
from app.schemas import (
    ExerciseProgressStatus,
    ExerciseProgressToggle,
    WeeklyProgressItem,
    WorkoutDayProgressResponse,
)


router = APIRouter(prefix="/progress", tags=["Progress"])


def build_day_progress(workout_day: WorkoutDay, progress_date: date, user_id: int) -> WorkoutDayProgressResponse:
    progress_map = {
        progress.exercise_id: progress
        for progress in workout_day.exercise_progress
        if progress.user_id == user_id and progress.progress_date == progress_date
    }

    exercise_statuses = [
        ExerciseProgressStatus(
            exercise_id=exercise.id,
            exercise_name=exercise.name,
            is_completed=bool(progress_map.get(exercise.id) and progress_map[exercise.id].is_completed),
            completed_at=progress_map.get(exercise.id).completed_at if progress_map.get(exercise.id) else None,
        )
        for exercise in workout_day.exercises
    ]

    total_exercises = len(exercise_statuses)
    completed_exercises = sum(1 for exercise in exercise_statuses if exercise.is_completed)
    remaining_exercises = max(total_exercises - completed_exercises, 0)
    percentage = round((completed_exercises / total_exercises) * 100, 2) if total_exercises else 0.0

    return WorkoutDayProgressResponse(
        day_name=workout_day.day_name,
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

    target_exercise = db.query(Exercise).filter(Exercise.id == payload.exercise_id).first()
    if not target_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    workout_day = (
        db.query(WorkoutDay)
        .filter(WorkoutDay.id == target_exercise.workout_day_id)
        .first()
    )

    progress = (
        db.query(ExerciseProgress)
        .filter(
            ExerciseProgress.user_id == current_user.id,
            ExerciseProgress.exercise_id == payload.exercise_id,
            ExerciseProgress.progress_date == progress_date,
        )
        .first()
    )

    if not progress:
        progress = ExerciseProgress(
            user_id=current_user.id,
            workout_day_id=workout_day.id,
            exercise_id=target_exercise.id,
            progress_date=progress_date,
        )
        db.add(progress)

    progress.is_completed = payload.is_completed
    progress.completed_at = datetime.now(timezone.utc) if payload.is_completed else None
    db.commit()
    db.refresh(workout_day)

    workout_day = (
        db.query(WorkoutDay)
        .filter(WorkoutDay.id == workout_day.id)
        .first()
    )
    return build_day_progress(workout_day, progress_date, current_user.id)


@router.get("/days/{day_name}", response_model=WorkoutDayProgressResponse)
def get_day_progress(
    day_name: str,
    progress_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_day = (
        db.query(WorkoutDay)
        .filter(WorkoutDay.day_name == day_name.strip().lower())
        .first()
    )
    if not workout_day:
        raise HTTPException(status_code=404, detail="Workout day not found")

    return build_day_progress(workout_day, progress_date or date.today(), current_user.id)


@router.get("/weekly", response_model=list[WeeklyProgressItem])
def get_weekly_progress(
    progress_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    selected_date = progress_date or date.today()
    workout_days = db.query(WorkoutDay).order_by(WorkoutDay.id.asc()).all()

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
