from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort

class BaseView(ModelView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "policy", None) == "admin"
        )

    def inaccessible_callback(self, name, **kwargs):
        abort(404)
