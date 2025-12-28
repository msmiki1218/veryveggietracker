from flask import render_template, request, jsonify, session, flash, redirect, url_for
from helpers import get_db, login_required 
from . import tracker_bp # Import the blueprint object

# The Main Dashboard Route (url_for('tracker.index'))
@tracker_bp.route("/")
@login_required
def index():
    # Fetch all 10 generations and the user's current progress
    db = get_db()
    cursor = db.cursor()

    # We calculate (Completed Goals / Total Goals) * 100 for the progress bar
    # Pass session["user_id"] directly as the next argument
    cursor.execute("""
        SELECT 
            generations.id, 
            generations.name, 
            generations.color_code, 
            generations.career,
            generations.aspiration,
            generations.requirements,
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

# The Dynamic Generation Route (url_for('tracker.generation_view', veggie_name='broccoli'))
@tracker_bp.route("/generation/<veggie_name>")
@login_required
def generation_view(veggie_name):
    db = get_db()
    cursor = db.cursor()

    # clean veggie_name so that it matches the table
    name = veggie_name.capitalize()

    # query generations table
    cursor.execute("SELECT * FROM generations WHERE name=?", (name,))
    veggie_row = cursor.fetchone()

    if veggie_row is None:
        flash("Veggie does not exist.")
        return redirect(url_for("tracker.index"))
    
    cursor.execute("""
        SELECT 
            goals.id, goals.description, user_progress.completed
        FROM goals 
        LEFT JOIN user_progress 
            ON goals.id = user_progress.goal_id
            AND user_progress.user_id = ?
        WHERE goals.generation_id = ?
    """, (session["user_id"],veggie_row["id"])
    )

    progress_list = cursor.fetchall()

    return render_template("generation.html", goals=progress_list, veggie=veggie_row)

# The AJAX Update Route (url_for('tracker.update_goal'))
@tracker_bp.route("/update_goal", methods=["POST"])
def update_goal():
    data = request.get_json()
    goal_id = data.get("goal_id")
    completed = data.get("completed")
    user_id = session.get("user_id")

    db = get_db()
    cursor = db.cursor()

    # The SQL "Upsert" logic
    cursor.execute("""
        INSERT INTO user_progress (user_id, goal_id, completed)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, goal_id) DO UPDATE SET
            completed = excluded.completed
    """, (user_id, goal_id, completed))
    
    db.commit()
    
    return jsonify({"success": True, "message": "Database updated!"})

@tracker_bp.route("/update_aspiration", methods=["POST"])
def update_aspiration():
    data = request.get_json()
    gen_id = data.get("gen_id")
    completed = data.get("completed")
    user_id = session.get("user_id")

    db = get_db()
    # We update the progress table for this specific vegetable generation
    db.execute("""
        UPDATE user_progress 
        SET aspiration_completed = ? 
        WHERE user_id = ? AND goal_id IN (
            SELECT id FROM goals WHERE generation_id = ?
        )
    """, (completed, user_id, gen_id))
    db.commit()
    
    return jsonify({"success": True})
    