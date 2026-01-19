from apps.admin.base import BaseView
from wtforms.fields import SelectField

class UserView(BaseView):

    form_excluded_columns = (
        'threads',
        'posts',
        'password_hash',
        'created_at',
        'updated_at',
    )

    form_overrides = {
        'policy': SelectField,
    }

    form_args = {
        'policy': {
            'choices': [
                ('user'),
                ('admin'),
            ]
        }
    }