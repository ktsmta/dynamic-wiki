from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from apps.main import main_bp
from apps.models import *
from apps import db

# スレッド一覧
@main_bp.route("/<slug>/thread/all")
def thread_all(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    threads = (
        Thread.query.filter_by(category_id=category.id)
        .order_by(Thread.created_at.desc())
        .all()
    )

    return render_template(
        "thread/thread_all.html",
        category=category,
        threads=threads
    )

# スレッド詳細
@main_bp.route("/<slug>/thread/<thread_id>", methods=["GET", "POST"])
def thread_detail(slug, thread_id):
    thread = Thread.query.get_or_404(thread_id)

    if thread.category.slug != slug:
        abort(404)

    if request.method == "POST":
        # ★ 投稿だけログイン必須
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        # 互換維持：content_md があれば優先、無ければ従来の content
        raw = (request.form.get("content_md") or request.form.get("content") or "")
        content = raw.strip()

        parent_id = request.form.get("parent_id") or None

        if not content:
            return redirect(url_for("main.thread_detail", slug=slug, thread_id=thread.id))

        post = Post(
            thread_id=thread.id,
            user_id=current_user.id,
            parent_id=parent_id,
            content=content,
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.thread_detail", slug=slug, thread_id=thread.id))

    posts = (
        Post.query
        .filter_by(thread_id=thread.id)
        .order_by(Post.created_at.asc())
        .all()
    )

    return render_template(
        "thread/thread_detail.html",
        thread=thread,
        posts=posts,
    )


""""
# スレッド詳細
@main_bp.route("/<slug>/threads/<thread_id>", methods=["GET", "POST"])
def thread_detail(slug, thread_id):
    thread = Thread.query.get_or_404(thread_id)

    if thread.category.slug != slug:
        abort(404)

    if request.method == "POST":
        # ★ 投稿だけログイン必須
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        content = (request.form.get("content") or "").strip()
        parent_id = request.form.get("parent_id") or None

        if not content:
            return redirect(url_for("main.thread_detail", slug=slug, thread_id=thread.id))

        post = Post(
            thread_id=thread.id,
            user_id=current_user.id,   # ← 追加（必須）
            parent_id=parent_id,
            content=content,
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.thread_detail", slug=slug, thread_id=thread.id))

    posts = (
        Post.query
        .filter_by(thread_id=thread.id)
        .order_by(Post.created_at.asc())
        .all()
    )

    return render_template(
        "thread/thread_detail.html",
        thread=thread,
        posts=posts,
    )
"""

# スレッド新規作成
@main_bp.route('/<slug>/thread/new', methods=["GET", "POST"])
@login_required
def thread_new(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        thread_type = (request.form.get("thread_type") or "question").strip()

        allowed_types = {"question", "discussion"}
        if thread_type not in allowed_types:
            thread_type = "question"  # MVPは強制でOK（厳密に弾くなら abort(400) など）

        # 最低限のバリデーション
        if not title or not content:
            return render_template("thread/thread_new.html", category=category)

        thread = Thread(
            title=title,
            category_id=category.id,
            user_id=current_user.id,
            thread_type=thread_type,  # ← 追加したカラム（A案：question/discussion）
        )
        db.session.add(thread)
        db.session.flush()

        first_post = Post(
            thread_id=thread.id,
            user_id=current_user.id,
            parent_id=None,
            content=content,
        )
        db.session.add(first_post)
        db.session.commit()

        return redirect(url_for("main.thread_detail", slug=slug, thread_id=thread.id))

    return render_template("thread/thread_new.html", category=category)