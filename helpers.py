import os
import sys
import sqlite3
import shutil # Added for copying the database
from flask import redirect, session, url_for, g
from functools import wraps

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 1. Database Connection Helper (Desktop-Optimized)
def get_db():
    if 'db' not in g:
        # Define where the permanent data should live
        data_dir = os.path.expanduser("~/Documents/VeggieTracker")
        perm_db_path = os.path.join(data_dir, "veggie.db")
        
        # Define where the 'starter' database is inside the app bundle
        bundle_db_path = resource_path("veggie.db")

        # Create the Documents folder if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # MIGRATION: If no database exists in Documents, copy the one from the app
        if not os.path.exists(perm_db_path):
            shutil.copy2(bundle_db_path, perm_db_path)

        # Connect to the PERMANENT version in Documents
        g.db = sqlite3.connect(perm_db_path)
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