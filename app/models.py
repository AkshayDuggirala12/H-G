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
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    plan_assignment: Mapped["UserPlanAssignment | None"] = relationship(
        "UserPlanAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    exercise_progress: Mapped[list["UserExerciseProgress"]] = relationship(
        "UserExerciseProgress",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    access_requests: Mapped[list["ClientAccessRequest"]] = relationship(
        "ClientAccessRequest",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="ClientAccessRequest.created_at.desc()",
    )


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    days: Mapped[list["WorkoutPlanDay"]] = relationship(
        "WorkoutPlanDay",
        back_populates="workout_plan",
        cascade="all, delete-orphan",
        order_by="WorkoutPlanDay.sort_order",
    )
    assignments: Mapped[list["UserPlanAssignment"]] = relationship(
        "UserPlanAssignment",
        back_populates="workout_plan",
    )


class WorkoutPlanDay(Base):
    __tablename__ = "workout_plan_days"
    __table_args__ = (
        UniqueConstraint("workout_plan_id", "day_name", name="uq_workout_plan_day_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_plan_id: Mapped[int] = mapped_column(ForeignKey("workout_plans.id"), nullable=False, index=True)
    day_name: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    video_url: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    workout_plan: Mapped[WorkoutPlan] = relationship("WorkoutPlan", back_populates="days")
    exercises: Mapped[list["WorkoutPlanExercise"]] = relationship(
        "WorkoutPlanExercise",
        back_populates="workout_day",
        cascade="all, delete-orphan",
        order_by="WorkoutPlanExercise.id",
    )
    progress_entries: Mapped[list["UserExerciseProgress"]] = relationship(
        "UserExerciseProgress",
        back_populates="workout_day",
        cascade="all, delete-orphan",
    )


class WorkoutPlanExercise(Base):
    __tablename__ = "workout_plan_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_day_id: Mapped[int] = mapped_column(ForeignKey("workout_plan_days.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sets: Mapped[str] = mapped_column(String(50), nullable=False)
    reps: Mapped[str] = mapped_column(String(50), nullable=False)

    workout_day: Mapped[WorkoutPlanDay] = relationship("WorkoutPlanDay", back_populates="exercises")
    progress_entries: Mapped[list["UserExerciseProgress"]] = relationship(
        "UserExerciseProgress",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )


class DietPlan(Base):
    __tablename__ = "diet_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    meals: Mapped[list["DietMeal"]] = relationship(
        "DietMeal",
        back_populates="diet_plan",
        cascade="all, delete-orphan",
        order_by="DietMeal.id",
    )
    assignments: Mapped[list["UserPlanAssignment"]] = relationship(
        "UserPlanAssignment",
        back_populates="diet_plan",
    )


class DietMeal(Base):
    __tablename__ = "diet_meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    diet_plan_id: Mapped[int] = mapped_column(ForeignKey("diet_plans.id"), nullable=False, index=True)
    meal_name: Mapped[str] = mapped_column(String(100), nullable=False)
    meal_time: Mapped[str] = mapped_column(String(50), nullable=False)
    foods: Mapped[str] = mapped_column(Text, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)

    diet_plan: Mapped[DietPlan] = relationship("DietPlan", back_populates="meals")


class UserPlanAssignment(Base):
    __tablename__ = "user_plan_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False, index=True)
    workout_plan_id: Mapped[int | None] = mapped_column(ForeignKey("workout_plans.id"), nullable=True, index=True)
    diet_plan_id: Mapped[int | None] = mapped_column(ForeignKey("diet_plans.id"), nullable=True, index=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="plan_assignment")
    workout_plan: Mapped[WorkoutPlan | None] = relationship("WorkoutPlan", back_populates="assignments")
    diet_plan: Mapped[DietPlan | None] = relationship("DietPlan", back_populates="assignments")


class UserExerciseProgress(Base):
    __tablename__ = "user_exercise_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", "progress_date", name="uq_user_plan_exercise_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    workout_day_id: Mapped[int] = mapped_column(ForeignKey("workout_plan_days.id"), nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("workout_plan_exercises.id"), nullable=False, index=True)
    progress_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="exercise_progress")
    workout_day: Mapped[WorkoutPlanDay] = relationship("WorkoutPlanDay", back_populates="progress_entries")
    exercise: Mapped[WorkoutPlanExercise] = relationship("WorkoutPlanExercise", back_populates="progress_entries")


class ClientAccessRequest(Base):
    __tablename__ = "client_access_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_kg: Mapped[str] = mapped_column(String(20), nullable=False)
    height_cm: Mapped[str] = mapped_column(String(20), nullable=False)
    workout_frequency: Mapped[str] = mapped_column(String(100), nullable=False)
    goals: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="access_requests")
