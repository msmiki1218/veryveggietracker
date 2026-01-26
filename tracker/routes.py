import webview
from flask import render_template, request, jsonify, session, Blueprint
from helpers import get_db, login_required, resource_path

# ONLY define it here. Do not import it from . or __init__.py
tracker_bp = Blueprint('tracker', 
    __name__, 
    template_folder=resource_path('tracker/templates')
)

@tracker_bp.route("/quit")
def quit_app():
    active_window = webview.active_window()
    if active_window:
        active_window.destroy()
    return "Quitting..."

# The Main Dashboard Route
@tracker_bp.route("/")
@login_required
def index():
    db = get_db()
    cursor = db.cursor()

    # Pass session["user_id"] to filter progress for the specific user
    cursor.execute("""
        SELECT 
            generations.id, 
            generations.name, 
            generations.color_code, 
            generations.career,
            generations.aspiration,
            generations.traits,
            COALESCE(SUM(user_progress.completed), 0) AS completed_count,
            (SELECT COUNT(*) FROM goals WHERE goals.generation_id = generations.id) AS total_count,
            COALESCE(MAX(user_progress.aspiration_completed), 0) AS is_mastered
        FROM generations
        LEFT JOIN goals ON generations.id = goals.generation_id
        LEFT JOIN user_progress ON goals.id = user_progress.goal_id 
            AND user_progress.user_id = ?
        GROUP BY generations.id
    """, (session["user_id"],))

    generations = cursor.fetchall()
    return render_template("index.html", generations=generations)

# The Dynamic Generation Route
@tracker_bp.route("/generation/<veggie_name>")
@login_required
def generation_view(veggie_name):
    db = get_db()
    cursor = db.cursor()

    name = veggie_name.capitalize()

    # Query generations table
    cursor.execute("SELECT * FROM generations WHERE name=?", (name,))
    veggie_row = cursor.fetchone()

    # Your template should handle {% if not veggie %} to show an error message.
    if veggie_row is None:
        return render_template("generation.html", veggie=None)
    
    cursor.execute("""
        SELECT 
            goals.id, goals.description, user_progress.completed
        FROM goals 
        LEFT JOIN user_progress 
            ON goals.id = user_progress.goal_id
            AND user_progress.user_id = ?
        WHERE goals.generation_id = ?
    """, (session["user_id"], veggie_row["id"]))

    progress_list = cursor.fetchall()

    return render_template("generation.html", goals=progress_list, veggie=veggie_row)

# The AJAX Update Route (No changes needed here as it uses JSON)
@tracker_bp.route("/update_goal", methods=["POST"])
def update_goal():
    data = request.get_json()
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({"success": False, "message": "Session expired"}), 401

    goal_id = data.get("goal_id")
    completed = data.get("completed")

    db = get_db()
    db.execute("""
        INSERT INTO user_progress (user_id, goal_id, completed)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, goal_id) DO UPDATE SET
            completed = excluded.completed
    """, (user_id, goal_id, completed))
    db.commit()
    
    return jsonify({"success": True})

@tracker_bp.route("/update_aspiration", methods=["POST"])
def update_aspiration():
    data = request.get_json()
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({"success": False}), 401

    gen_id = data.get("gen_id")
    completed = data.get("completed")

    db = get_db()
    db.execute("""
        UPDATE user_progress 
        SET aspiration_completed = ? 
        WHERE user_id = ? AND goal_id IN (
            SELECT id FROM goals WHERE generation_id = ?
        )
    """, (completed, user_id, gen_id))
    db.commit()
    
    return jsonify({"success": True})
