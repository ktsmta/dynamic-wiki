from flask import Blueprint

forums_bp = Blueprint(
    "forums",
    __name__,
    template_folder="templates",
)

from apps.forums.routes import main
