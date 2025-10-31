from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from apps.core import core_bp
    from apps.admin import admin_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app