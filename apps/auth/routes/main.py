from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from apps.auth import auth_bp
from apps import db
from apps.models.user import User


def _safe_next(default_endpoint: str = "core.index") -> str:
    """
    next パラメータを優先してリダイレクトする。
    外部URLへのオープンリダイレクト対策として、ここでは「相対パスのみ」許可。
    """
    next_url = request.args.get("next") or request.form.get("next") or ""
    if next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return url_for(default_endpoint)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("メールアドレスとパスワードを入力してください。", "error")
            return render_template("auth/login.html", next=request.form.get("next", ""))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("メールアドレスまたはパスワードが違います。", "error")
            return render_template("auth/login.html", next=request.form.get("next", ""))

        login_user(user)
        flash("ログインしました。", "success")
        return redirect(_safe_next())

    return render_template("auth/login.html", next=request.args.get("next", ""))


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not email or not username or not password:
            flash("未入力の項目があります。", "error")
            return render_template("auth/signup.html", next=request.form.get("next", ""))

        if len(username) < 2 or len(username) > 50:
            flash("ユーザー名は 2〜50 文字で入力してください。", "error")
            return render_template("auth/signup.html", next=request.form.get("next", ""))

        if len(password) < 8:
            flash("パスワードは 8 文字以上にしてください。", "error")
            return render_template("auth/signup.html", next=request.form.get("next", ""))

        if User.query.filter_by(email=email).first():
            flash("このメールアドレスは既に登録されています。", "error")
            return render_template("auth/signup.html", next=request.form.get("next", ""))

        if User.query.filter_by(username=username).first():
            flash("このユーザー名は既に使用されています。", "error")
            return render_template("auth/signup.html", next=request.form.get("next", ""))

        user = User(email=email, username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("アカウントを作成しました。", "success")
        return redirect(_safe_next())

    return render_template("auth/signup.html", next=request.args.get("next", ""))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("ログアウトしました。", "success")
    return redirect(url_for("core.index"))
