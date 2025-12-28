from flask import Blueprint

# Define the blueprint object
# 'tracker' is the name used for url_for (e.g., url_for('tracker.index'))
# __name__ is the current Python module
# template_folder points to the templates directory inside the tracker folder
tracker_bp = Blueprint('tracker', __name__, template_folder='templates')

# Import the routes so the application can find them
from . import routes