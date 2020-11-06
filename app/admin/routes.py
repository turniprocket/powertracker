from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from pwgen import pwgen
from app import db
from app.admin import bp
from app.models import User, Group
from app.auth.group_check import group_check
from app.admin.forms import AddUserForm, DeleteUserForm, AddGroupForm, DeleteGroupForm, AddToGroupForm, RemoveFromGroupForm

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
@group_check(role='administrators')
def dashboard():
    add_user_form = AddUserForm()
    delete_user_form = DeleteUserForm()
    add_group_form = AddGroupForm()
    delete_group_form = DeleteGroupForm()
    add_to_group_form = AddToGroupForm()
    remove_from_group_form = RemoveFromGroupForm()

    user_list = User.query.order_by(User.username).all()

    if add_user_form.add_user_submit.data and add_user_form.validate_on_submit():
        new_user = User(username=add_user_form.username.data, email=add_user_form.email.data)
        group = Group.query.filter_by(group_name=add_user_form.group.data).first()
        temp_password = pwgen(10, symbols=True)
        new_user.set_password(temp_password)
        new_user.password_expired = True
        db.session.add(new_user)
        new_user.add_to_group(group)
        db.session.commit()

        flash('User ' + new_user.username + ' has been added with the temporary password: ' + temp_password)
        return redirect(url_for('admin.dashboard'))

    if delete_user_form.delete_user_submit.data and delete_user_form.validate_on_submit():
        user = User.query.filter_by(username=delete_user_form.username.data).first()
        groups = user.list_groups()
        for g in groups:
            user.remove_from_group(g)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
        flash('User ' + user.username + ' has been deleted.')
        return redirect(url_for('admin.dashboard'))

    if add_group_form.add_group_submit.data and add_group_form.validate_on_submit():
        group = Group(group_name=add_group_form.group_name.data)
        db.session.add(group)
        db.session.commit()
        flash('Group ' + group.group_name + ' has been added.')
        return redirect(url_for('admin.dashboard'))

    if delete_group_form.delete_group_submit.data and delete_group_form.validate_on_submit():
        group_to_delete = Group.query.filter_by(group_name=delete_group_form.group_name.data).first()
        users = group_to_delete.list_users()
        for u in users:
            u.remove_from_group(group)
            db.session.commit()
        db.session.delete(group)
        db.session.commit()
        flash('Group ' + group.group_name + ' has been deleted.')
        return redirect(url_for('admin.dashboard'))

    if add_to_group_form.add_to_group_submit.data and add_to_group_form.validate_on_submit():
        user = User.query.filter_by(username=add_to_group_form.username.data).first()
        group = Group.query.filter_by(group_name=add_to_group_form.group_name.data).first()
        user.add_to_group(group)
        db.session.commit()
        flash('User ' + user.username + ' has been added to the group named ' + group.group_name +'.')
        return redirect(url_for('admin.dashboard'))

    if remove_from_group_form.remove_from_group_submit.data and remove_from_group_form.validate_on_submit():
        user = User.query.filter_by(username=remove_from_group_form.username.data).first()
        group = Group.query.filter_by(group_name=remove_from_group_form.group_name.data).first()
        user.remove_from_group(group)
        db.session.commit()
        flash('User ' + user.username + ' has been removed from the group ' + group.group_name + '.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/dashboard.html', title='Admin Dashboard', add_user_form=add_user_form, \
                            delete_user_form=delete_user_form, add_group_form=add_group_form, delete_group_form=delete_group_form, \
                            add_to_group_form=add_to_group_form, remove_from_group_form=remove_from_group_form, user_list=user_list)