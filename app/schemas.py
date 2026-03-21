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

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ExerciseResponse(BaseModel):
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
    exercises: list[ExerciseResponse]

    model_config = ConfigDict(from_attributes=True)


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
