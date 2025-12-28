from flask import Blueprint

# 1. Define the blueprint
# 'auth' is the name used for url_for (e.g., url_for('auth.login'))
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# 2. Import the routes so Flask knows they exist
# This must be at the BOTTOM to avoid circular imports
from . import routes