#!/usr/bin/python3
"""
Task module
"""

from datetime import datetime
from .basemodel import BaseModel
from .. import db


class Task(BaseModel):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=True)  # Set a default value if needed
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # Use an Enum field for status

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    group = db.relationship('Group', backref=db.backref('tasks', lazy=True))
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.id}: {self.task_name}>'