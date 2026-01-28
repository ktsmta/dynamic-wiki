# apps/init.py

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from markdown import markdown as md_to_html
import bleach

# インスタンス化
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # DB設定
    db_path = os.path.join(app.instance_path, "local.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CSRF用シークレットキー
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["WTF_CSRF_SECRET_KEY"] = os.getenv("WTF_CSRF_SECRET_KEY")

    # 各拡張機能を初期化
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # モデル読み込み
    from apps.models import category, thread, post, wiki

    # Blueprint登録
    # core
    from apps.core import core_bp
    app.register_blueprint(core_bp,)

    # login
    from apps.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # admin
    from apps.admin import admin_bp, init_admin
    app.register_blueprint(admin_bp, url_prefix='/admin')
    init_admin(app)

    # main
    from apps.main import main_bp
    app.register_blueprint(main_bp, url_prefix='/wiki')

    # search
    from apps.search import search_bp
    app.register_blueprint(search_bp)

    # account
    from apps.account import account_bp
    app.register_blueprint(account_bp)



    # 不正なスクリプト送信防止
    ALLOWED_TAGS = [
        "p", "br",
        "strong", "em", "del",
        "blockquote",
        "code", "pre",
        "ul", "ol", "li",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "a", "img",
    ]

    ALLOWED_ATTRS = {
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt", "title"],
        "code": ["class"],
        "pre": ["class"],
    }

    ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

    def render_md(text: str) -> str:
        if not text:
            return ""

        # Markdown -> HTML
        html = md_to_html(
            text,
            extensions=[
                "fenced_code",   # ```code```
                "tables",
                "nl2br",         # 改行を <br> に
            ],
            output_format="html5",
        )

        # HTML sanitize
        cleaned = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
        )

        # linkify（URLを自動リンク化）
        cleaned = bleach.linkify(cleaned)

        return cleaned

    app.jinja_env.filters["render_md"] = render_md

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    return app