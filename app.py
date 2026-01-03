import os
import sqlite3
import webview
from flask import Flask, g
from auth.routes import auth_bp
from tracker.routes import tracker_bp
from helpers import resource_path

# --- FLASK INITIALIZATION ---
app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

# 1. Set the Secret Key
app.config['SECRET_KEY'] = 'dev_key_for_sims_tracker_123' 

# 2. Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tracker_bp)

# Refresh the dashboard every time user looks at it
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 3. Database cleanup
@app.teardown_appcontext
def close_connection(exception):
    # This looks for 'db' inside the Flask 'g' object and closes it if it exists
    db_conn = getattr(g, 'db', None)
    if db_conn is not None:
        db_conn.close()
# --- END FLASK INITIALIZATION ---

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)