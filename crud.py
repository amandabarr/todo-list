from model import db, List, Task


def create_todo_list(name):
    todo_list = List(name=name)

    db.session.add(todo_list)
    db.session.commit()
    return todo_list


def create_task(name, is_completed=False):
    task = Task(name=name, is_completed=is_completed)

    db.session.add(task)
    db.session.commit()

    return task


if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
