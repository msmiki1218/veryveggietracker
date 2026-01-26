from flask import render_template, request, redirect, url_for, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_db, resource_path

# Define the blueprint correctly for your folder structure
auth_bp = Blueprint(
    'auth', 
    __name__, 
    template_folder=resource_path("auth/templates")
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    cursor = db.cursor()
    error = None

    # Clear session on every login attempt for security
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "All fields are required!"
            return render_template("login.html", error=error)
             
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Invalid username or password."
            return render_template("login.html", error=error)
        
        # Log user in
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("tracker.index"))
    
    return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    cursor = db.cursor()
    error = None

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # 1. Validation
        if not username or not password or not confirmation:
            error = "All fields are required!"
            return render_template("register.html", error=error)

        if password != confirmation:
            error = "Passwords do not match."
            return render_template("register.html", error=error)

        # 2. Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            error = "Username already taken."
            return render_template("register.html", error=error)

        # 3. Create User
        hash_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_pw))
        
        # Get the ID of the new user using lastrowid (more efficient)
        new_user_id = cursor.lastrowid

        # 4. Initialize User Progress
        # We grab all goals and link them to the new user with '0' completion
        cursor.execute("SELECT id FROM goals")
        all_goals = cursor.fetchall()

        # Batch insert for better performance
        for goal in all_goals:
            cursor.execute(
                "INSERT INTO user_progress (user_id, goal_id, completed) VALUES (?, ?, 0)", 
                (new_user_id, goal["id"])
            )

        # Final commit for user and all progress rows
        db.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html", error=error)