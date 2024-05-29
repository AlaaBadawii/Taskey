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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Group {self.id}: {self.group_name}>'
