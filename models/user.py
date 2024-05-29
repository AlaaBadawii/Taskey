#!/usr/bin/python3
"""
User model
"""
from datetime import datetime
from passlib.hash import pbkdf2_sha256 
from .basemodel import BaseModel
from flask_login import UserMixin
from .. import db

class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Renamed to password_hash
    email = db.Column(db.String(120), unique=True, nullable=False)

    groups = db.relationship('Group', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='task_user', lazy=True)


    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)  # Hashing the password

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)  # Verifying the password
