# apps/search/routes/main.py
from flask import request, render_template, redirect, url_for
from sqlalchemy import or_

from apps.search import search_bp
from apps.models.category import Category
from apps.models.thread import Thread
from apps.models.post import Post


@search_bp.get("/")
def result():
    q = (request.args.get("q") or "").strip()
    if not q:
        return redirect(url_for("main.category_all"))

    like = f"%{q}%"

    categories = (
        Category.query
        .filter(or_(
            Category.name.ilike(like),
            Category.slug.ilike(like),
        ))
        .limit(50)
        .all()
    )

    threads = (
        Thread.query
        .filter(Thread.title.ilike(like))
        .order_by(Thread.created_at.desc())
        .limit(50)
        .all()
    )

    posts = (
        Post.query
        .filter(Post.content.ilike(like))
        .order_by(Post.created_at.desc())
        .limit(50)
        .all()
    )

    return render_template(
        "search/result.html",
        q=q,
        categories=categories,
        threads=threads,
        posts=posts,
    )
