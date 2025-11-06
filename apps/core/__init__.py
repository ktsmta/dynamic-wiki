from flask import Blueprint

core_bp = Blueprint(
    'core',
    __name__,
    template_folder='templates',
)

from apps.core.routes import main