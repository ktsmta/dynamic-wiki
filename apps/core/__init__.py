from flask import Blueprint

core_bp = Blueprint(
    'core',
    __name__,
    template_folder='templates',
    static_folder='static',
)

from apps.core.routes import main