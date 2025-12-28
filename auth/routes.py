import sqlite3
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_db  # Assuming your SQL object is in helpers
from . import auth_bp  # Import the blueprint object from __init__.py

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    cursor = db.cursor()

    # Start with no error
    error = None

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username or not password:
            error = "All fields are required!"
            return render_template("login.html", error=error)
             
        # Query database for username
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )

        # use fetchone() instead of checking length
        user = cursor.fetchone()

        # Ensure username exists and password is correct
        # 'user' will be None if the username isn't found
        if user is None or not check_password_hash(user["hash"], password):
            error = "Invalid username or password."
            return render_template("login.html", error=error)
        
        # Remember which user has logged in
        # With row_factory, we can access by name
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("tracker.index"))
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    error = None

    if request.method == "POST":
        username = request.form.get("username")
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
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            error = "Username already taken."
            return render_template("register.html", error=error)

        # 3. Hash password and insert into DB
        hash_pw = generate_password_hash(password)
        # Inserting a new user
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        
        # IMPORTANT: You must commit for changes to save!
        db.commit()
        
        # Get the ID of the user we just created
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        new_user_id = user_row["id"]

        # Get all goal IDs from the goals table
        cursor.execute("SELECT id FROM goals")
        all_goals = cursor.fetchall()

        # Insert a row for every goal for this specific user
        for goal in all_goals:
            cursor.execute(
                "INSERT INTO user_progress (user_id, goal_id, completed) VALUES (?, ?, 0)", 
                (new_user_id, goal["id"])
            )

        # Final commit for the user_progress entries
        db.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html", error=error)