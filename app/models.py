import base64
from datetime import datetime, timedelta
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

group_membership = db.Table(
    'group_membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.String(10), default='Never')
    password_expired = db.Column(db.Boolean)
    groups = db.relationship(
        'Group',
        secondary=group_membership,
        primaryjoin=(group_membership.c.user_id == id),
        backref=db.backref('group_membership', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_to_group(self, group):
        if not self.in_group(group):
            self.groups.append(group)

    def remove_from_group(self, group):
        if self.in_group(group):
            self.groups.remove(group)

    def in_group(self, group):
        return self.groups.filter(
            group_membership.c.group_id == group.id).count() > 0

    def list_groups(self):
        in_groups = Group.query.join(
            group_membership, (group_membership.c.user_id == self.id)).filter(
                group_membership.c.user_id == self.id)
        return in_groups.order_by(Group.id.desc())

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(32), index=True, unique=True)
    members = db.relationship(
        'User',
        secondary=group_membership,
        primaryjoin=(group_membership.c.group_id == id),
        backref=db.backref('group_membership', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return '<Group: {}>'.format(self.group_name)

    def list_users(self):
        users = User.query.join(
            group_membership, (group_membership.c.group_id == self.id)).filter(
                group_membership.c.group_id == self.id)
        return users.order_by(User.id.desc())

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))