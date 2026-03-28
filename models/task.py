#!/usr/bin/python3
"""
Task module
"""

from datetime import date, datetime
from .basemodel import BaseModel
from .. import db
from .group import Group

class Task(BaseModel):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    task_title = db.Column(db.String(255), nullable=False)
    task_description = db.Column(db.String(1024), nullable=False)
    due_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    priority = db.Column(db.String(20), nullable=False, default="low")
    status = db.Column(db.String(20), nullable=False, default="pending")
    steps = db.Column(db.String(1024), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)


    def __repr__(self):
        return f'<Task {self.id}: {self.task_name}>'

    @property
    def is_missed(self):
        return (
            self.status != 'completed'
            and self.due_date is not None
            and self.due_date < date.today()
        )

    @property
    def display_status(self):
        if self.is_missed:
            return 'missed'
        return self.status
