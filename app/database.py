from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        inspector = inspect(connection)
        if "users" not in inspector.get_table_names():
            return

        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "is_admin" not in user_columns:
            if engine.dialect.name == "postgresql":
                connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE"))
            else:
                connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))

        if "workout_plan_exercises" in inspector.get_table_names():
            exercise_columns = {column["name"] for column in inspector.get_columns("workout_plan_exercises")}
            if "gif_url" not in exercise_columns:
                connection.execute(
                    text("ALTER TABLE workout_plan_exercises ADD COLUMN gif_url VARCHAR(500) NOT NULL DEFAULT ''")
                )
            if "instructions" not in exercise_columns:
                connection.execute(
                    text("ALTER TABLE workout_plan_exercises ADD COLUMN instructions TEXT NOT NULL DEFAULT ''")
                )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
