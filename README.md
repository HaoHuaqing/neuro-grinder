## hello
- This is crud app based on python3.5,flask,flask-appbuilder.
- You need complete subject and task form first, then complete visit form.
- File upload to /app/static/.

## Table encounter
subject_id(f), timestamp, side_tested, ?pre_after, task_id, csv_location


## Table subject
subject_id, name, sex, dob, side_affected, stroke_date, stroke_location


## Table task
task_id, name, description


## TODO
- Github everything on devlop
- Correct the tables
- Generate JSON-encoded .csv filenames based on queries (all pre trials for LateralReaching

## run
Create an Admin user::

    $ fabmanager create-admin

Run it::

    $ fabmanager run
