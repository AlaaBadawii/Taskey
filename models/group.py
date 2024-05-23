#!/usr/bin/python3
"""
Group model
"""

from .basemodel import BaseModel
from datetime import datetime
from .. import db

class Group(BaseModel):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='task_group', lazy=True)

    def __repr__(self):
        return f'<Group {self.id}: {self.group_name}>'
