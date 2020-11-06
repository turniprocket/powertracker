from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User, Group
from app.main import bp
from app.auth.group_check import group_check
from app.auth.forms import ChangePasswordForm, ChangeEmailForm

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@group_check(role='public')
def index():
    return render_template('index.html', title='Home')

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@group_check(role='public')
def settings():
    change_password_form = ChangePasswordForm()
    change_email_form = ChangeEmailForm()
    group = Group.query.filter_by(group_name='administrators').first()
    user = User.query.filter_by(username=current_user.username).first()

    if change_password_form.validate_on_submit():
        if user is not None or user.check_password(change_password_form.old_password.data):
            user.set_password(change_password_form.new_password.data)
            db.session.commit()
            flash('Your password has been changed.')
            return redirect(url_for('main.settings'))
        else:
            flash('Incorrect passwords or passwords did not match.')
            return redirect(url_for('main.settings'))

    if change_email_form.validate_on_submit():
        if user is not None or user.check_password(change_email_form.password.data):
            user.email = change_email_form.new_email.data
            db.session.commit()
            flash('Your email has been updated.')
            return redirect(url_for('main.settings'))
        else:
            flash('Incorrect password.')
            return redirect(url_for('main.settings'))
            
    return render_template('settings.html', title='My Settings', user=user, group=group, change_password_form=change_password_form, \
                            change_email_form=change_email_form)