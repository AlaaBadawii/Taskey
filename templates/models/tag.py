#!/usr/bin/python3
"""
Tag model
"""

from .basemodel import BaseModel
from .. import db

class Tag(BaseModel):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)  # Removed nullable=False
    tag_name = db.Column(db.String(50), nullable=False, unique=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    task = db.relationship('Task', backref=db.backref('tags', lazy=True))

    def __repr__(self):
        return f'<Tag {self.id}: {self.tag_name}>'

