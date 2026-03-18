from sqlalchemy.orm import Session

from app.models import Exercise, WorkoutDay


WORKOUT_SEED = [
    {
        "day_name": "monday",
        "title": "Legs Workout",
        "description": "Focus on quads, hamstrings, glutes, and calves.",
        "video_url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
        "exercises": [
            {"name": "Barbell Squat", "sets": "4", "reps": "8-10"},
            {"name": "Leg Press", "sets": "3", "reps": "10-12"},
            {"name": "Walking Lunges", "sets": "3", "reps": "12 each leg"},
        ],
    },
    {
        "day_name": "tuesday",
        "title": "Chest Workout",
        "description": "Build chest strength and upper-body power.",
        "video_url": "https://www.youtube.com/watch?v=VmB1G1K7v94",
        "exercises": [
            {"name": "Bench Press", "sets": "4", "reps": "8-10"},
            {"name": "Incline Dumbbell Press", "sets": "3", "reps": "10-12"},
            {"name": "Cable Fly", "sets": "3", "reps": "12-15"},
        ],
    },
    {
        "day_name": "wednesday",
        "title": "Lats Workout",
        "description": "Target the lats and widen the back.",
        "video_url": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
        "exercises": [
            {"name": "Lat Pulldown", "sets": "4", "reps": "10-12"},
            {"name": "Seated Row", "sets": "3", "reps": "10-12"},
            {"name": "Straight Arm Pulldown", "sets": "3", "reps": "12-15"},
        ],
    },
    {
        "day_name": "thursday",
        "title": "Shoulder Workout",
        "description": "Train front, side, and rear delts.",
        "video_url": "https://www.youtube.com/watch?v=qEwKCR5JCog",
        "exercises": [
            {"name": "Overhead Press", "sets": "4", "reps": "8-10"},
            {"name": "Lateral Raise", "sets": "3", "reps": "12-15"},
            {"name": "Rear Delt Fly", "sets": "3", "reps": "12-15"},
        ],
    },
    {
        "day_name": "friday",
        "title": "Back And Legs Workout",
        "description": "A heavier split for posterior chain and legs.",
        "video_url": "https://www.youtube.com/watch?v=roCP6wCXPqo",
        "exercises": [
            {"name": "Deadlift", "sets": "4", "reps": "5-6"},
            {"name": "Romanian Deadlift", "sets": "3", "reps": "8-10"},
            {"name": "Leg Curl", "sets": "3", "reps": "12"},
        ],
    },
    {
        "day_name": "saturday",
        "title": "Hands Workout",
        "description": "Train biceps, triceps, and forearms.",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "exercises": [
            {"name": "Barbell Curl", "sets": "4", "reps": "10-12"},
            {"name": "Tricep Pushdown", "sets": "4", "reps": "10-12"},
            {"name": "Hammer Curl", "sets": "3", "reps": "12"},
        ],
    },
    {
        "day_name": "sunday",
        "title": "Active Rest Day",
        "description": "Light walking, mobility work, stretching, and recovery.",
        "video_url": "https://www.youtube.com/watch?v=L_xrDAtykMI",
        "exercises": [
            {"name": "Walking", "sets": "1", "reps": "20-30 min"},
            {"name": "Mobility Flow", "sets": "1", "reps": "10-15 min"},
            {"name": "Stretching", "sets": "1", "reps": "10 min"},
        ],
    },
]


def seed_workouts(db: Session) -> None:
    already_seeded = db.query(WorkoutDay).first()
    if already_seeded:
        return

    for day in WORKOUT_SEED:
        workout_day = WorkoutDay(
            day_name=day["day_name"],
            title=day["title"],
            description=day["description"],
            video_url=day["video_url"],
        )

        for exercise in day["exercises"]:
            workout_day.exercises.append(
                Exercise(
                    name=exercise["name"],
                    sets=exercise["sets"],
                    reps=exercise["reps"],
                )
            )

        db.add(workout_day)

    db.commit()
