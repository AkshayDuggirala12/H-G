from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exercise_progress: Mapped[list["ExerciseProgress"]] = relationship(
        "ExerciseProgress",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    day_name: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    video_url: Mapped[str] = mapped_column(String(255), nullable=False)

    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="workout_day",
        cascade="all, delete-orphan",
    )
    exercise_progress: Mapped[list["ExerciseProgress"]] = relationship(
        "ExerciseProgress",
        back_populates="workout_day",
        cascade="all, delete-orphan",
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_day_id: Mapped[int] = mapped_column(ForeignKey("workout_days.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sets: Mapped[str] = mapped_column(String(50), nullable=False)
    reps: Mapped[str] = mapped_column(String(50), nullable=False)

    workout_day: Mapped[WorkoutDay] = relationship("WorkoutDay", back_populates="exercises")
    progress_entries: Mapped[list["ExerciseProgress"]] = relationship(
        "ExerciseProgress",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )


class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", "progress_date", name="uq_user_exercise_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    workout_day_id: Mapped[int] = mapped_column(ForeignKey("workout_days.id"), nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
    progress_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="exercise_progress")
    workout_day: Mapped[WorkoutDay] = relationship("WorkoutDay", back_populates="exercise_progress")
    exercise: Mapped[Exercise] = relationship("Exercise", back_populates="progress_entries")
