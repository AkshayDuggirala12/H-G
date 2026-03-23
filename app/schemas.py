from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class WorkoutExerciseCreate(BaseModel):
    name: str
    sets: str
    reps: str


class WorkoutDayCreate(BaseModel):
    day_name: str
    title: str
    description: str
    video_url: str = ""
    exercises: list[WorkoutExerciseCreate]


class WorkoutPlanCreate(BaseModel):
    name: str
    description: str = ""
    days: list[WorkoutDayCreate]


class WorkoutExerciseResponse(BaseModel):
    id: int
    name: str
    sets: str
    reps: str

    model_config = ConfigDict(from_attributes=True)


class WorkoutDayResponse(BaseModel):
    id: int
    day_name: str
    title: str
    description: str
    video_url: str
    exercises: list[WorkoutExerciseResponse]

    model_config = ConfigDict(from_attributes=True)


class WorkoutPlanResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    days: list[WorkoutDayResponse]

    model_config = ConfigDict(from_attributes=True)


class DietMealCreate(BaseModel):
    meal_name: str
    meal_time: str
    foods: str
    notes: str = ""


class DietPlanCreate(BaseModel):
    name: str
    description: str = ""
    meals: list[DietMealCreate]


class DietMealResponse(BaseModel):
    id: int
    meal_name: str
    meal_time: str
    foods: str
    notes: str

    model_config = ConfigDict(from_attributes=True)


class DietPlanResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    meals: list[DietMealResponse]

    model_config = ConfigDict(from_attributes=True)


class AssignedPlansResponse(BaseModel):
    workout_plan: WorkoutPlanResponse | None = None
    diet_plan: DietPlanResponse | None = None


class UserPlanAssignmentRequest(BaseModel):
    workout_plan_id: int | None = None
    diet_plan_id: int | None = None


class UserPlanAssignmentResponse(BaseModel):
    user: UserResponse
    workout_plan: WorkoutPlanResponse | None = None
    diet_plan: DietPlanResponse | None = None
    assigned_at: datetime


class UserSummaryResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    workout_plan_id: int | None = None
    diet_plan_id: int | None = None


class ExerciseProgressToggle(BaseModel):
    exercise_id: int
    is_completed: bool
    progress_date: date | None = None


class ExerciseProgressStatus(BaseModel):
    exercise_id: int
    exercise_name: str
    is_completed: bool
    completed_at: datetime | None = None


class WorkoutDayProgressResponse(BaseModel):
    day_name: str
    title: str
    progress_date: date
    completed_exercises: int
    total_exercises: int
    remaining_exercises: int
    percentage: float
    is_day_completed: bool
    exercises: list[ExerciseProgressStatus]


class WeeklyProgressItem(BaseModel):
    day_name: str
    title: str
    progress_date: date
    completed_exercises: int
    total_exercises: int
    remaining_exercises: int
    percentage: float
    is_day_completed: bool
