from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from apps import db
from apps.models.category import Category
from apps.models.thread import Thread
from apps.models.post import Post
from apps.models.wiki import Wiki
from apps.models.user import User

from apps.admin.views.index import AdminOnlyIndexView
from apps.admin.views.category import CategoryView
from apps.admin.views.thread import ThreadView
from apps.admin.views.post import PostView
from apps.admin.views.wiki import WikiView
from apps.admin.views.user import UserView

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    template_folder='templates',
)

def init_admin(app):
    admin = Admin(
        app,
        index_view=AdminOnlyIndexView(),
    )

    admin.add_view(CategoryView(Category, db.session))
    admin.add_view(ThreadView(Thread, db.session))
    admin.add_view(PostView(Post, db.session))
    admin.add_view(WikiView(Wiki, db.session))
    admin.add_view(UserView(User, db.session))

    return admin
