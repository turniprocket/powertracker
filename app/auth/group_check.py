from flask import redirect, url_for
from flask_login import current_user
from app import db
from app.models import User, Group
from functools import wraps

def group_check(role):
    def required_group(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not role == 'public':
                group = Group.query.filter_by(group_name=role).first()
                if not current_user.in_group(group):
                    return redirect(url_for('main.index'))
            return func(*args, **kwargs)
        return wrapper
    return required_group