from flask import Blueprint, render_template, request
from database import create_connection, DB_NAME, get_user_progress, get_user_notes_scores, get_grades_of_user

review_bp = Blueprint('review', __name__)

@review_bp.route('/')
def review():
    user_id = request.cookies.get('airsID')
    print(f"[DEBUG] User ID from cookie: {user_id}")

    try:
        conn = create_connection(DB_NAME)

        user_progress = get_user_progress(conn, user_id)
        print("[DEBUG] user_progress:", user_progress)
        average_grade = user_progress[1]

        notes_scores = get_user_notes_scores(conn, user_id)


        print("[DEBUG] notes_scores:", notes_scores)
        filtered = [note for note in notes_scores if note[2] > 0]
        best_note = max(filtered, key=lambda x: x[1] / x[2])
        preferred_note = best_note[0]
        # preferred_note = "C4"

        all_exercises = get_grades_of_user(conn, user_id)
        print("[DEBUG] all_exercises:", all_exercises)
        five_last_exercises = all_exercises[:5]

        conn.close()

        print("=== TEMPLATE CONTEXT ===")
        print("average_grade:", average_grade)
        print("preferred_note:", preferred_note)
        print("five_last_exercises:", five_last_exercises)


        return render_template('review.html',
                               average_grade=average_grade,
                               preferred_note=preferred_note,
                               five_last_exercises=five_last_exercises)

    except:
        return render_template('index.html', alert_message="Please complete at least 5 excercises before reviewing!")
