from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///todolist', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class List(db.Model):

    __tablename__ = "lists"

    list_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"List - List Name = {self.name}"


class Task(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Task - Task Name = {self.name} Completed = {self.is_completed}"


class ListTask(db.Model):

    __tablename__ = "list_tasks"

    list_task_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True
                             )
    list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'),
                        nullable=False)
    task_id = db.Column(db.Integer,
                        db.ForeignKey('tasks.task_id'),
                        nullable=False)

    list = db.relationship("List", backref="lists")
    task = db.relationship("Task", backref="tasks")

    def __repr__(self):
        return f"ListTask - List_Task_ID = {self.list_task_id} List_ID = {self.list_id} Task_ID = {self.task_id}"


def setup_tables():
    db.create_all()

    test_list1 = List(name="Groceries")
    db.session.add(test_list1)
    test_list2 = List(name="Morning Checklist")
    db.session.add(test_list2)

    task1 = Task(name="Oranges")
    db.session.add(task1)
    task2 = Task(name="Onions")
    db.session.add(task2)
    task3 = Task(name="Brush Teeth")
    db.session.add(task3)

    db.session.commit()


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    setup_tables()
