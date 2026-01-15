from flask import render_template
from apps.main import main_bp
from apps.models import *
from apps import db

# All
@main_bp.route('/')
def category_all():
    categories = Category.query.filter(Category.parent_id.is_(None)).all()
    return render_template(
        'category/category_all.html',
        categories=categories,
    )

# detail
@main_bp.route('/<slug>')
def category_detail(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    parent = category.parent
    children = category.children
    latest_threads = (
        Thread.query
        .filter_by(category_id=category.id)
        .order_by(Thread.created_at.desc())
        .limit(5)
        .all()
    )
    wiki = category.wiki

    return render_template(
        "category/category_detail.html",
        category=category,
        parent=parent,
        children=children,
        latest_threads=latest_threads,
        wiki=wiki,
    )