from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Group

def validate_username_not_exist(FlaskForm, field):
    user = User.query.filter_by(username=field.data).first()
    if user is not None:
        raise ValidationError('A user with this username is already exists.')

def validate_username_exist(FlaskForm, field):
    user = User.query.filter_by(username=field.data).first()
    if user is None:
        raise ValidationError('That username does not exist.')

def validate_email_not_exist(FlaskForm, field):
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        raise ValidationError('A user with this email already exists.')

def validate_email_exist(FlaskForm, field):
    user = User.query.filter_by(email=field.data).first()
    if user is None:
        raise ValidationError('A user wtih this email does not exist.')

def validate_group_not_exist(FlaskForm, field):
    group = Group.query.filter_by(group_name=field.data).first()
    if group is not None:
        raise ValidationError('A group with this name is already exists.')

def validate_group_exist(FlaskForm, field):
    group = Group.query.filter_by(group_name=field.data).first()
    if group is None:
        raise ValidationError('That group does not exist.')

def validate_confirm(FlaskForm, field):
    if not field.data:
        raise ValidationError('Confirm box not checked.')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_username_not_exist])
    email = StringField('Email', validators=[DataRequired(), Email(), validate_email_not_exist])
    group = StringField('Group', validators=[DataRequired(), validate_group_exist])
    add_user_submit = SubmitField('Add User')

class DeleteUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_username_exist])
    confirm = BooleanField('Confirm deletion', validators=[validate_confirm])
    delete_user_submit = SubmitField('Delete User')

class AddGroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired(), validate_group_not_exist])
    add_group_submit = SubmitField('Add Group')

class DeleteGroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired(), validate_group_exist])
    confirm = BooleanField('Confirm deletion', validators=[validate_confirm])
    delete_group_submit = SubmitField('Delete Group')

class AddToGroupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_username_exist])
    group_name = StringField('Group Name', validators=[DataRequired(), validate_group_exist])
    add_to_group_submit = SubmitField('Add To Group')

class RemoveFromGroupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_username_exist])
    group_name = StringField('Group Name', validators=[DataRequired(), validate_group_exist])
    remove_from_group_submit = SubmitField('Remove From Group')