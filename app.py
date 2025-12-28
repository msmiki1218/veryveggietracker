import os
from flask import Flask
from auth.routes import auth_bp
from tracker.routes import tracker_bp

app = Flask(__name__)

# 1. Set the Secret Key
# In development, you can use a string. In production, use an environment variable.
app.config['SECRET_KEY'] = 'dev_key_for_sims_tracker_123' 

# 2. Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tracker_bp)

# refresh the dashboard every time user looks at it
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or not cache.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 3. Database cleanup
@app.teardown_appcontext
def close_connection(exception):
    from helpers import g
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)