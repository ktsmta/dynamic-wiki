from flask import render_template, abort
from apps.categories import categories_bp
from apps.models.category import Category

@categories_bp.route("/<slug>")
def category_top(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        abort(404)

    return render_template("categories/category_top.html", category=category)
