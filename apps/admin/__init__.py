from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from apps import db
from apps.models.category import Category
from apps.models.thread import Thread
from apps.models.post import Post
from apps.models.wiki import Wiki

from apps.admin.category_view import CategoryAdmin

admin_bp = Blueprint(
    "admin_bp",
    __name__,
)

def init_admin(app):
    admin = Admin(app, name="Dynamic Wiki 管理者専用")

    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(ModelView(Thread, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Wiki, db.session))

    return admin
