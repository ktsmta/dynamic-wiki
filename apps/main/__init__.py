from flask import Blueprint

main_bp = Blueprint(
    'main',
    __name__,
    template_folder='templates',
)

from apps.main.routes import category
from apps.main.routes import thread
from apps.main.routes import media