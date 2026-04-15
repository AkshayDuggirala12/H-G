from sqlalchemy.orm import Session

from app.models import DietMeal, DietPlan, WorkoutPlan, WorkoutPlanDay, WorkoutPlanExercise


def _exercise(name: str, sets: str, reps: str, gif_url: str = "", instructions: str = "") -> dict[str, str]:
    return {
        "name": name,
        "sets": sets,
        "reps": reps,
        "gif_url": gif_url,
        "instructions": instructions,
    }


DEFAULT_WORKOUT_PLAN = {
    "name": "Starter Strength Plan",
    "description": "Weekly gym routine with GIF previews for each exercise.",
    "days": [
        {
            "day_name": "monday",
            "title": "Legs + Cardio",
            "description": "Start with treadmill warmup, then lower-body strength and finish with cardio conditioning.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Back Squat", "4", "10-12", "https://share.google/cU1GXTuFJcwRLhizW", "Keep your chest up, brace your core, and drive through your heels."),
                _exercise("Leg Curl", "4", "15", "https://share.google/sqtL000Gy7WLcqZg1", "Move slowly and squeeze the hamstrings at the top."),
                _exercise("Hip Thrust Machine", "4", "15", "https://share.google/ePY2P7XjHgSiQiF56", "Pause at the top and keep your chin tucked."),
                _exercise("Leg Extension Machine", "5", "10-12", "https://share.google/yUFQqnFc6uLDinAwa", "Lift under control and avoid swinging the weight."),
                _exercise("Adductor Inner Leg Machine", "6", "12-15", "https://share.google/yL7zA48mQSp3ERnrH", "Squeeze the inner thighs at the end of each rep."),
                _exercise("Adductor Outer Machine", "3", "12-15", "https://share.google/lQmP3QqOEQ5mS5gEw", "Control the movement and do not rush the return."),
                _exercise("Leg Press Machine", "2", "10-12", "https://share.google/jhsbwBANC30yv3tCf", "Keep your back flat and push through the heels."),
                _exercise("Leg Calf Raise Machine", "4", "10-12", "https://share.google/3N14B61hKsNpKGiTt", "Pause at the top and fully stretch the calves."),
                _exercise("Stationary Cycling", "1", "15 mins", "https://share.google/mJlyiXASbY32uAJoI", "Use steady pace for the cardio finish."),
                _exercise("Rowing Machine", "1", "15 mins", "https://share.google/pcn2weJjkacBa2etY", "Keep smooth pulls and strong posture."),
                _exercise("Battle Ropes", "4", "30 sec each, total 2 min", "https://share.google/Q4QqtH0CEb0JVVXTU", "Use fast, controlled rope waves."),
                _exercise("Kettlebell Swings", "4", "25 swings", "https://share.google/wBK9kDfA87fmKDX7I", "Hinge at the hips and let the kettlebell swing from momentum."),
            ],
        },
        {
            "day_name": "tuesday",
            "title": "Shoulders + Abs",
            "description": "Treadmill warmup, assisted pull-up work, shoulders, then abs.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Shoulder Assisted Pull Ups Machine", "1", "Warmup", "", "Use as a warm-up before the shoulder session."),
                _exercise("Seated Shoulder Press", "5", "10-12", "https://share.google/AgK6QSD5rZWVn0dKE", "Start light, press overhead with control, and increase weight only if the form stays clean."),
                _exercise("Cable Rope Face Pulls", "4", "12-15", "https://share.google/xaYuMuo4H4QQeWqkO", "Pull toward the face and keep elbows high."),
                _exercise("Dumbbell Front Raise", "4", "13-16", "https://share.google/IwAYzfo15WIi24TRt", "Raise the dumbbells to shoulder height without swinging."),
                _exercise("Dumbbell Lateral Raise", "4", "10-12", "https://share.google/GuxmJB2hK2K687mJ5", "Lift out to the sides with a slight bend in the elbows."),
                _exercise("Dumbbell Punches", "5", "10-15 punches each side", "https://share.google/72Qs8Tw8y5fgF0Khp", "Keep the punches controlled and stable."),
                _exercise("Plank Toe Touches", "4", "10 each side", "https://share.google/TEoB660Ug0W70lONF", "Hold your core tight while tapping the opposite toe."),
                _exercise("Flutter Kicks", "3", "30 sec", "https://share.google/NwU14cV1Awx4HirQu", "Keep the lower back flat and feet moving continuously."),
                _exercise("Side Plank With Oblique Crunch", "2", "10 each side", "https://share.google/w3pc9DEG6kDBQlDAj", "Drive the elbow toward the knee with control."),
                _exercise("Frog Crunch", "3", "12-15", "https://share.google/lUteLEmNviPYPoP6F", "Crunch up using your abs and keep the movement short."),
            ],
        },
        {
            "day_name": "wednesday",
            "title": "Back + Side Abs",
            "description": "Warmup, back work, then side abdominals and core stability.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Back Assisted Pull Ups Machine", "1", "15 reps total 50 assistance needed", "", "Use the assistance level that lets you complete the reps with clean form."),
                _exercise("Lat Pulldown Front", "4", "12-15", "https://share.google/mxCUej9BXDlMSMGRy", "Pull to upper chest and keep your torso stable."),
                _exercise("Lat Pulldown Back", "4", "12-15", "https://share.google/SAlcKT6pz9pKybn54", "Use a controlled range and avoid jerking the bar."),
                _exercise("Seated Cable Row", "4", "15-17", "https://share.google/cInTtaAZTDMApdsiB", "Squeeze the shoulder blades together on every pull."),
                _exercise("One Arm Dumbbell Row", "4", "8-12", "https://share.google/2341eAVLyijQhdKUm", "Row toward the hip and keep the back flat."),
                _exercise("Close Grip Lat Pulldown", "4", "10-12", "https://share.google/P3if3uQKbqAC1ZUS8", "Use the lats to pull and do not lean too far back."),
                _exercise("Back Extensions", "5", "8-10", "https://share.google/2ZahqyQohzM7d05Ut", "Lift with the lower back and glutes, not momentum."),
                _exercise("Bicycle Crunches", "4", "10 each side", "https://share.google/X4QWbULT7pa6bCaZF", "Rotate through the torso and keep the abs tight."),
                _exercise("High Knees", "3", "25 each side", "https://share.google/9vfkAzSHpdNr2vGLX", "Drive knees up quickly while staying on the balls of your feet."),
                _exercise("Plank", "4", "20 sec", "https://share.google/ymm9311xkDwkcyaj2", "Keep hips level and brace the core."),
            ],
        },
        {
            "day_name": "thursday",
            "title": "Hands + Cardio",
            "description": "Warmup, biceps and triceps work, then a cardio circuit.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Back Assisted Pull Ups Machine", "1", "15 reps total 50 assistance needed", "", "Warm up before arms training."),
                _exercise("Biceps Assisted Pull Up Machine", "5", "10 reps", "", "Use controlled reps and avoid swinging."),
                _exercise("Supinated Biceps Curl", "4", "8-10", "https://share.google/SW4LqaMwdY8reRCS1", "Curl with palms up and keep elbows close to the body."),
                _exercise("Dumbbell Skull Crushers", "4", "8-10", "https://share.google/2e7XL0ayWnZ7w0ihV", "Lower the dumbbells slowly and keep the elbows steady."),
                _exercise("Hammer Curls", "4", "10-12", "https://share.google/UxBzZv1XO0OqZdVvE", "Keep neutral grip and lift without swinging."),
                _exercise("Tricep Pushdowns With Rope", "4", "8-10", "https://share.google/OyZpwpu0G1y1IhVVK", "Push down fully and spread the rope at the bottom."),
                _exercise("Preacher Curl Machine", "4", "10-12", "https://share.google/Wmr3auX8VQe9J4Z6N", "Keep the upper arm fixed on the pad."),
                _exercise("Dumbbell Tricep Kickback", "10", "Each side", "https://share.google/LqkAF7dsqvpFmhiEu", "Extend fully and pause at the end of each rep."),
                _exercise("Concentration Curl", "4", "10-12", "https://share.google/xhFHYB5CROmMPvJoY", "Curl slowly and squeeze the biceps at the top."),
                _exercise("Triceps Bench Dips", "3", "10-12", "https://share.google/m1wnY5sEzfukNNwej", "Keep shoulders down and elbows tracking back."),
                _exercise("Jumping Jacks", "4", "25 reps", "https://share.google/pGND3gJA3rT70j2wv", "Use a fast steady rhythm."),
                _exercise("Mountain Climbers", "4", "15 each side", "https://share.google/OM3YuvkHlxJtd1d0U", "Keep hips low and drive knees forward."),
                _exercise("High Knees Workout", "4", "15 each side", "https://share.google/pbh4BRZT7AsUhEtmg", "Stay light on your feet and move quickly."),
                _exercise("Jump Squats", "4", "8-10", "https://share.google/IuO7xeIygqYkZIfFj", "Land softly and keep the chest lifted."),
                _exercise("Cycling", "1", "15-20 mins", "https://share.google/34TIIfIKT0RG4W7fA", "Maintain a steady pace throughout."),
                _exercise("Side Plank", "4", "15 sec", "https://share.google/LjYcwmQmUVI8JwmUF", "Hold the hips high and keep the body straight."),
            ],
        },
        {
            "day_name": "friday",
            "title": "Chest + Abs",
            "description": "Warmup, chest pressing, chest fly work, and ab training.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Back Assisted Pull Ups Machine", "1", "15 reps total 50 assistance needed", "", "Warm up before chest pressing."),
                _exercise("Chest Assisted Pull Up Machine", "5", "10 reps", "", "Use a stable controlled pull."),
                _exercise("Flat Barbell Bench Press", "4", "10-12", "https://share.google/kJc35TE7zgwtmWc8q", "Keep the shoulders packed and press straight up."),
                _exercise("Flat Fly Machine", "3", "12-15", "https://share.google/oSmKKpuM7V1Bcsod2", "Move through the chest with a controlled squeeze."),
                _exercise("Incline Barbell Bench Press", "4", "10-12", "https://share.google/3PjXtQCATufmuPKR6", "Press from the upper chest with steady control."),
                _exercise("Incline Bench Dumbbell Chest Fly", "4", "7-9", "https://share.google/gjqw45DaayqSOA3bi", "Use a slow stretch and controlled squeeze."),
                _exercise("Decline Barbell Bench Press", "4", "10-12", "https://share.google/BbbU2362ZCo6CR0rn", "Lower the bar with control and keep wrists stacked."),
                _exercise("Cable Decline Bench Chest Fly", "4", "10-12", "https://share.google/bvHmfQNq5FrNaTOZH", "Keep tension on the chest through the full range."),
                _exercise("Ab Crunch Machine", "5", "15", "https://share.google/RQnOD5neta6wybHC1", "Crunch through the abs and avoid pulling with the arms."),
                _exercise("Dumbbell Side Bend", "3", "10", "https://share.google/PhtaP1SAZUBNoGvSS", "Bend only at the waist and keep the movement controlled."),
                _exercise("Sit Ups", "3", "10", "https://share.google/axqO4pnID62NaMmEQ", "Use the core to lift the torso."),
                _exercise("Knee-Up", "3", "10", "https://share.google/DZhaPJ8WSINSXjQSL", "Bring knees in with control and keep the abs engaged."),
            ],
        },
        {
            "day_name": "saturday",
            "title": "Full Body Strength + Cardio",
            "description": "Warmup, heavy glute and leg work, pull-up work, and finish with cycling.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill Warmup", "1", "5 min walk + 1 min jog + 2 min walk + 2 min run", "", "5 mins walking at 5.5 speed, 1 min jogging at 7 speed, 2 mins walking at 4.5 speed, then 2 mins running at 8 or 9 speed."),
                _exercise("Back Assisted Pull Ups Machine", "1", "15 reps total 50 assistance needed", "", "Warm up before the strength work."),
                _exercise("Hip Thrusts", "2", "6-8", "https://share.google/FNj9unKX5PUbnkVlw", "Use the highest safe weight and pause at the top."),
                _exercise("Inner Leg Machine", "2", "6-8", "https://share.google/VsJEAa0BOdAXFjnAR", "Perform the movement with control and strong squeeze."),
                _exercise("Deadlifts", "3", "5-6", "https://share.google/neI3Xrm6c8D7X8X86", "Keep the bar close to the body and brace the core."),
                _exercise("Shoulder Assisted Pull Ups Machine", "5", "10 reps", "https://share.google/qxY0LHLgWHAC7rkXM", "Pull with control and use the right assistance level."),
                _exercise("Back Assisted Pull Ups Machine", "5", "10 reps", "https://share.google/bhlsmehwd9NUxhBD7", "Keep the movement smooth and controlled."),
                _exercise("Heel-Elevated Goblet Squats", "4", "6-7", "https://share.google/3hMqqINSnRv3zlr2i", "Keep the chest upright and squat deep with control."),
                _exercise("Lateral Box Step-Ups", "3", "10 each side", "https://share.google/8RIjKgzRoP4BaH8WM", "Drive through the working leg and keep balance steady."),
                _exercise("Kettlebell Swings", "3", "20", "https://share.google/FZgGWDtH8vuYMdWbU", "Hinge at the hips and snap the kettlebell through the swing."),
                _exercise("Half Kneeling Overhead Presses", "3", "10 each side", "https://share.google/9qFVEZ5xv3mohO3Bp", "Press overhead while keeping the torso tight."),
                _exercise("Cycling", "1", "10-15 mins", "", "Use the bike as your finishing cardio."),
            ],
        },
        {
            "day_name": "sunday",
            "title": "Cardio + Recovery",
            "description": "Treadmill cardio, cycling, and lower-back recovery work.",
            "video_url": "",
            "exercises": [
                _exercise("Treadmill", "1", "40 mins", "", "2 mins normal walking speed 4, 2-10 mins speed 4 incline 8, 10-15 mins speed 5 incline 0, 15-25 mins speed 4.5 incline 7, 25-37 mins speed 4 incline 9, 37-40 mins speed 3 incline 0."),
                _exercise("Cycling", "1", "10 mins level 10", "", "Keep the pace steady and controlled."),
                _exercise("Back Hyperextension Machine", "6", "10 reps", "", "Move through the back extensors and keep the spine neutral."),
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
                        gif_url=exercise["gif_url"],
                        instructions=exercise["instructions"],
                    )
                )
    else:
        workout_plan.description = DEFAULT_WORKOUT_PLAN["description"]
        workout_day_map = {workout_day.day_name: workout_day for workout_day in workout_plan.days}

        for index, day in enumerate(DEFAULT_WORKOUT_PLAN["days"]):
            workout_day = workout_day_map.get(day["day_name"])
            if not workout_day:
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
            else:
                workout_day.title = day["title"]
                workout_day.description = day["description"]
                workout_day.video_url = day["video_url"]
                workout_day.sort_order = index

            existing_exercises = {exercise.name: exercise for exercise in workout_day.exercises}
            desired_exercise_names = {exercise["name"] for exercise in day["exercises"]}
            for exercise in day["exercises"]:
                workout_exercise = existing_exercises.get(exercise["name"])
                if not workout_exercise:
                    db.add(
                        WorkoutPlanExercise(
                            workout_day_id=workout_day.id,
                            name=exercise["name"],
                            sets=exercise["sets"],
                            reps=exercise["reps"],
                            gif_url=exercise["gif_url"],
                            instructions=exercise["instructions"],
                        )
                    )
                    continue

                workout_exercise.sets = exercise["sets"]
                workout_exercise.reps = exercise["reps"]
                workout_exercise.gif_url = exercise["gif_url"]
                workout_exercise.instructions = exercise["instructions"]

            for exercise_name, workout_exercise in list(existing_exercises.items()):
                if exercise_name not in desired_exercise_names:
                    workout_day.exercises.remove(workout_exercise)

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
