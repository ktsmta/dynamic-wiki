# apps/search/init.py

from flask import Blueprint
from apps.models import *

search_bp = Blueprint(
    "search",
    __name__,
    template_folder="templates",
)

from apps.search.routes import main