from flask_admin.contrib.sqla import ModelView

class CategoryAdmin(ModelView):
    form_excluded_columns = ('children', 'threads', 'created_at', 'updated_at')
