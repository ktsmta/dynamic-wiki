# apps/account/init.py

from flask import Blueprint
from apps.models import *

account_bp = Blueprint(
    "account",
    __name__,
    template_folder="templates",
)

from .routes import main