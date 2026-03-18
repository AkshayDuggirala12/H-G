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
