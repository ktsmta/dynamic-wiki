from flask import render_template, abort
from flask_login import login_required, current_user
from apps.account import account_bp
from apps.models.user import User

@account_bp.get('/@<string:username>')
def account(username: str):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    
    return render_template(
        'account/account.html',
        user=user,
    )