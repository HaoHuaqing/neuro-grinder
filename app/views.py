from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Task, Subject, side_tested, pre_after, Visit
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app import appbuilder, db

def fill_side_tested():
    try:
        db.session.add(side_tested(name='Left'))
        db.session.add(side_tested(name='Right'))
        db.session.commit()
    except:
        db.session.rollback()

def fill_pre_after():
    try:
        db.session.add(pre_after(name='Pre'))
        db.session.add(pre_after(name='After'))
        db.session.commit()
    except:
        db.session.rollback()

class SubjectView(ModelView):
    datamodel = SQLAInterface(Subject)

    list_columns = ['name', 'sex', 'side_affected']

    show_template = 'appbuilder/general/model/show_cascade.html'


class TaskView(ModelView):
    datamodel = SQLAInterface(Task)

    list_columns = ['name', 'description']

    show_template = 'appbuilder/general/model/show_cascade.html'

class VisitView(ModelView):
    datamodel = SQLAInterface(Visit)

    list_columns = ['subject', 'pre_after', 'task', 'location']

    show_template = 'appbuilder/general/model/show_cascade.html'

db.create_all()
fill_side_tested()
fill_pre_after()

appbuilder.add_view(SubjectView, "Subject", icon="fa-folder-open-o", category="Experiment")
appbuilder.add_separator("Experiment")
appbuilder.add_view(TaskView, "Task", icon="fa-folder-open-o", category="Experiment")
appbuilder.add_separator("Experiment")
appbuilder.add_view(VisitView, "Visit", icon="fa-folder-open-o", category="Experiment")
