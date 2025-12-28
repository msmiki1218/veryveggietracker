import sqlite3
from flask import redirect, session, url_for, g
from functools import wraps

# 1. Database Connection Helper
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("veggie.db")
        # This line allows you to access columns by name: row['username']
        g.db.row_factory = sqlite3.Row
    return g.db

# 2. Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function