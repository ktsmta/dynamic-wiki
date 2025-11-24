from flask import render_template
from apps.core import core_bp

from apps.models.category import Category

@core_bp.route("/")
def index():
    categories = Category.query.filter_by(parent_id=None).all()
    return render_template("core/index.html", categories=categories)

@core_bp.route("/robots.txt")
def robots_txt():
    return core_bp.send_static_file("meta/robots.txt")

@core_bp.route('/llms.txt')
def llms_txt():
    return core_bp.send_static_file("meta/llms.txt")