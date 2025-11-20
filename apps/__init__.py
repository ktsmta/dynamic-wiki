import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

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
    
    # モデル読み込み
    from apps.models import category, thread, post, wiki

    # Blueprint登録
    # core
    from apps.core import core_bp
    app.register_blueprint(core_bp, url_prefix="/")

    # admin
    from apps.admin import admin_bp, init_admin
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # categories
    from apps.categories import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/category')

    init_admin(app)

    return app
