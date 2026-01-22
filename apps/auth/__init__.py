# apps/auth/init.py

from flask import Blueprint
from apps.models.user import User
from apps import login_manager

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
)

login_manager.login_view = 'auth.login'
login_manager.login_message = ''

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(user_id)

from apps.auth.routes import main