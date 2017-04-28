import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

from flask_appbuilder.models.mixins import FileColumn
from flask import Markup, url_for

class Task(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500))


    def __repr__(self):
        return self.name

class side_tested(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class pre_after(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

class Subject(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    sex = Column(String(50))
    dob = Column(Date, default=datetime.date.today()) 
    side_affected = Column(String(50))
    stroke_date = Column(Date, default=datetime.date.today())
    stroke_location = Column(String(100))

    def __repr__(self):
        return self.name

class Visit(Model):
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    subject = relationship("Subject")
    side_tested_id = Column(Integer, ForeignKey('side_tested.id'), nullable=False)
    side_tested = relationship("side_tested")
    pre_after_id = Column(Integer, ForeignKey('pre_after.id'), nullable=False)
    pre_after = relationship("pre_after")
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    task = relationship("Task")
    time_stamp = Column(Date, default=datetime.date.today(), nullable=False)
    csv_location = Column(FileColumn, nullable=False)
    description = Column(String(500))

    def location(self):
        return str("C:\code\\neuro-grinder\\app\static\\uploads" + self.csv_location)
    def __repr__(self):
        return self.subject
