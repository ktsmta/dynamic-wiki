from flask import render_template
from apps.core import core_bp

@core_bp.route("/")
def index():
    return render_template("core/index.html")