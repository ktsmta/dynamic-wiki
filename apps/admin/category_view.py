from flask_admin.contrib.sqla import ModelView

class CategoryAdmin(ModelView):
    form_excluded_columns = ('children', 'wiki', 'threads', 'created_at', 'updated_at')
