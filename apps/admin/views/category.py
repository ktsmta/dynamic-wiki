from apps.admin.base import BaseView

class CategoryView(BaseView):
    
    form_excluded_columns = (
        'children',
        'wiki',
        'threads',
        'created_at',
        'updated_at',
    )
