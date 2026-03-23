from sqlalchemy.orm import Session

from app.models import DietMeal, DietPlan, WorkoutPlan, WorkoutPlanDay, WorkoutPlanExercise


DEFAULT_WORKOUT_PLAN = {
    "name": "Starter Strength Plan",
    "description": "A balanced weekly beginner-friendly gym routine.",
    "days": [
        {
            "day_name": "monday",
            "title": "Legs",
            "description": "Focus on lower-body strength and stability.",
            "video_url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
            "exercises": [
                {"name": "Barbell Squat", "sets": "4", "reps": "10-12"},
                {"name": "Leg Press", "sets": "3", "reps": "10-12"},
                {"name": "Leg Curl", "sets": "3", "reps": "12-15"},
            ],
        },
        {
            "day_name": "tuesday",
            "title": "Chest",
            "description": "Push-day chest and accessory work.",
            "video_url": "https://www.youtube.com/watch?v=VmB1G1K7v94",
            "exercises": [
                {"name": "Bench Press", "sets": "4", "reps": "8-10"},
                {"name": "Incline Dumbbell Press", "sets": "3", "reps": "10-12"},
                {"name": "Cable Fly", "sets": "3", "reps": "12-15"},
            ],
        },
        {
            "day_name": "wednesday",
            "title": "Back",
            "description": "Pull-day back and lat development.",
            "video_url": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
            "exercises": [
                {"name": "Lat Pulldown", "sets": "4", "reps": "10-12"},
                {"name": "Seated Row", "sets": "3", "reps": "10-12"},
                {"name": "Straight Arm Pulldown", "sets": "3", "reps": "12-15"},
            ],
        },
    ],
}


DEFAULT_DIET_PLAN = {
    "name": "Starter High Protein Diet",
    "description": "A simple daily meal structure for gym users.",
    "meals": [
        {
            "meal_name": "Breakfast",
            "meal_time": "08:00 AM",
            "foods": "Oats, milk, banana, and boiled eggs",
            "notes": "Keep it protein-focused.",
        },
        {
            "meal_name": "Lunch",
            "meal_time": "01:00 PM",
            "foods": "Rice, chicken breast, dal, and vegetables",
            "notes": "Add salad if available.",
        },
        {
            "meal_name": "Dinner",
            "meal_time": "08:00 PM",
            "foods": "Chapati, paneer or fish, and vegetables",
            "notes": "Keep dinner lighter than lunch.",
        },
    ],
}


def seed_default_plans(db: Session) -> None:
    workout_plan = db.query(WorkoutPlan).filter(WorkoutPlan.name == DEFAULT_WORKOUT_PLAN["name"]).first()
    if not workout_plan:
        workout_plan = WorkoutPlan(
            name=DEFAULT_WORKOUT_PLAN["name"],
            description=DEFAULT_WORKOUT_PLAN["description"],
        )
        db.add(workout_plan)
        db.flush()

        for index, day in enumerate(DEFAULT_WORKOUT_PLAN["days"]):
            workout_day = WorkoutPlanDay(
                workout_plan_id=workout_plan.id,
                day_name=day["day_name"],
                title=day["title"],
                description=day["description"],
                video_url=day["video_url"],
                sort_order=index,
            )
            db.add(workout_day)
            db.flush()

            for exercise in day["exercises"]:
                db.add(
                    WorkoutPlanExercise(
                        workout_day_id=workout_day.id,
                        name=exercise["name"],
                        sets=exercise["sets"],
                        reps=exercise["reps"],
                    )
                )

    diet_plan = db.query(DietPlan).filter(DietPlan.name == DEFAULT_DIET_PLAN["name"]).first()
    if not diet_plan:
        diet_plan = DietPlan(
            name=DEFAULT_DIET_PLAN["name"],
            description=DEFAULT_DIET_PLAN["description"],
        )
        db.add(diet_plan)
        db.flush()

        for meal in DEFAULT_DIET_PLAN["meals"]:
            db.add(
                DietMeal(
                    diet_plan_id=diet_plan.id,
                    meal_name=meal["meal_name"],
                    meal_time=meal["meal_time"],
                    foods=meal["foods"],
                    notes=meal["notes"],
                )
            )

    db.commit()
