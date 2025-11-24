from flask import render_template,request, redirect, url_for, abort
from apps.forums import forums_bp
from apps.models.category import Category
from apps.models.thread import Thread
from apps.models.post import Post
from apps import db

@forums_bp.route("/<slug>")
def category(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        abort(404)

    threads = Thread.query.filter_by(category_id=category.id).all()

    return render_template(
        "forums/category.html",
        category=category,
        threads=threads,
        children=category.children,
    )

@forums_bp.route("/<slug>/threads")
def thread_list(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    threads = Thread.query.filter_by(category_id=category.id).all()

    return render_template(
        "forums/thread_list.html",
        category=category,
        threads=threads
    )

@forums_bp.route("/<slug>/threads/<thread_id>")
def thread_detail(slug, thread_id):
    thread = Thread.query.get_or_404(thread_id)
    posts = thread.posts  
    return render_template("forums/thread_detail.html", thread=thread, posts=posts)

@forums_bp.route('/<slug>/threads/new', methods=["GET", 'POST'])
def thread_new(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        abort(404)
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # Thread 作成
        thread = Thread(title=title, category_id=category.id)
        db.session.add(thread)
        db.session.commit()   # 先に保存しないと thread.id が作られない

        # 最初の Post（親投稿）作成
        first_post = Post(
            thread_id=thread.id,
            parent_id=None,   # 最初の投稿
            content=content,
        )
        db.session.add(first_post)
        db.session.commit()

        return redirect(
            url_for("forums.thread_detail", slug=slug, thread_id=thread.id)
        )

    return render_template("forums/thread_new.html", category=category)