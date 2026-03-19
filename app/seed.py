from sqlalchemy.orm import Session

from app.models import Exercise, WorkoutDay


WORKOUT_SEED = [
    {
        "day_name": "monday",
        "title": "Legs Workout",
        "description": "Focus on quads, hamstrings, glutes, and calves.",
        "video_url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
        "exercises": [
            {"name": "Barbell Squat", "sets": "4", "reps": "10-12"},
            {"name": "Leg Extension", "sets": "4", "reps": "10-12"},
            {"name": "Hamstring leg Curls", "sets": "4", "reps": "10-12"}, 
            {"name": "Leg Press", "sets": "3", "reps": "10-12"},
            {"name": "inner legs ( gym staring untadi)", "sets": "4", "reps": "12-15"},
            {"name": "hip thrusts", "sets": "4", "reps": "15-20"},
        ],
    },
    {
        "day_name": "tuesday",
        "title": "Chest Workout",
        "description": "Build chest strength and upper-body power.",
        "video_url": "https://www.youtube.com/watch?v=VmB1G1K7v94",
        "exercises": [
            {"name": "flat Bench Press", "sets": "4", "reps": "10-12"},
            {"name": "Cable Fly ( gym starting lo untadi )", "sets": "4", "reps": "12-15"},
            {"name": "Incline Dumbbell Press", "sets": "4", "reps": "10-12"},
            {"name": "incline bench fly ", "sets": "4", "reps": "10-12"},
            {"name": "decline dumbbell press", "sets": "4", "reps": "12-15"},
            {"name": "cable decline fly ", "sets": "4", "reps": "12-15"},
        ],
    },
    {
        "day_name": "wednesday",
        "title": "Lats Workout",
        "description": "Target the lats and widen the back.",
        "video_url": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
        "exercises": [
            {"name": "Lat Pulldown (back)", "sets": "4", "reps": "12-15"},
            {"name": "Lat Pulldown (front)", "sets": "4", "reps": "12-15"},
            {"name": "Seated Row", "sets": "4", "reps": "15-20"},
            {"name": "T-Bar Row", "sets": "4", "reps": "10-12"},
            {"name": "Straight Arm Pulldown", "sets": "3", "reps": "12-15"},
        ],
    },
    {
        "day_name": "thursday",
        "title": "Shoulder Workout",
        "description": "Train front, side, and rear delts.",
        "video_url": "https://www.youtube.com/watch?v=qEwKCR5JCog",
        "exercises": [
            {"name": "Dumbbell Shoulder Press", "sets": "4", "reps": "10-15"},
            {"name": "Front Raise", "sets": "4", "reps": "10-12"},
            {"name": "weighted bar back sholder", "sets": "4", "reps": "10-12"},
            {"name": "Lateral Raise", "sets": "3", "reps": "12-15"},
            {"name": "Rear Delt Fly", "sets": "3", "reps": "12-15"},
            {"name": "Face Pull", "sets": "3", "reps": "12-15"},
            {"name": "Shrugs", "sets": "3", "reps": "15-20"},
        ],
    },
    {
        "day_name": "friday",
        "title": "Hands Workout",
        "description": "Train biceps, triceps, and forearms.",
        "video_url": "https://www.youtube.com/watch?v=roCP6wCXPqo",
        "exercises": [
            {"name": "Deadlift", "sets": "4", "reps": "5-8"},
            {"name": "bicple curl", "sets": "4", "reps": "10-12"},
            {"name": "Tricep Dips", "sets": "4", "reps": "10-12"},
            {"name": "Hammer Curl", "sets": "3", "reps": "12-15"},
            {"name": "Tricep Extension", "sets": "3", "reps": "12-15"},
            {"name": "preacher curl", "sets": "3", "reps": "12-15"},
            {"name": "single hand tricep extension", "sets": "3", "reps": "12-15"},
        ],
    },
    {
        "day_name": "saturday",
        "title": "abbs Workout",
        "description": "Train your core with focused abs exercises.",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "exercises": [
            {"name": "abb crunches", "sets": "4", "reps": "15-20"},
            {"name": "leg raises", "sets": "4", "reps": "15-20"},
            {"name": "bicycle crunches", "sets": "3", "reps": "15-20"},
            {"name": "Russian Twists", "sets": "3", "reps": "20-30"},
            {"name": "mountain climbers", "sets": "3", "reps": "30-60 sec"},
            {"name": "planks", "sets": "2", "reps": "30-60 sec"},
             
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
    existing_days = {
        workout_day.day_name: workout_day
        for workout_day in db.query(WorkoutDay).all()
    }
    seed_day_names = {day["day_name"] for day in WORKOUT_SEED}

    for stale_day_name, stale_day in list(existing_days.items()):
        if stale_day_name not in seed_day_names:
            db.delete(stale_day)

    for day in WORKOUT_SEED:
        workout_day = existing_days.get(day["day_name"])
        if not workout_day:
            workout_day = WorkoutDay(day_name=day["day_name"])
            db.add(workout_day)

        workout_day.title = day["title"]
        workout_day.description = day["description"]
        workout_day.video_url = day["video_url"]

        workout_day.exercises.clear()
        for exercise in day["exercises"]:
            workout_day.exercises.append(
                Exercise(
                    name=exercise["name"],
                    sets=exercise["sets"],
                    reps=exercise["reps"],
                )
            )

    db.commit()
