import json
from db import db, Task, Subtask, Category
from flask import Flask, request
import os

# define db filename
db_filename = "todo.db"
app = Flask(__name__)

# setup config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return os.environ['GOOGLE_CLIENT_ID'], 200

@app.route('/tasks/')
def get_tasks():
    tasks = Task.query.all()
    res = {'success': True, 'data': [task.serialize() for task in tasks]}
    return json.dumps(res), 200

@app.route('/tasks/', methods=['POST'])
def create_task():
    post_body = json.loads(request.data)
    task = Task(
        description=post_body.get('description'),
        done=bool(post_body.get('done'))
    )
    db.session.add(task)
    db.session.commit()
    return json.dumps({'success': True, 'data': task.serialize()}), 201

@app.route('/task/<int:task_id>/')
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found!'}), 404
    return json.dumps({'success': True, 'data': task.serialize()}), 200

@app.route('/task/<int:task_id>/', methods=['POST'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found!'}), 404
    post_body = json.loads(request.data)
    task.description = post_body.get('description', task.description)
    task.done = bool(post_body.get('done', task.done))
    db.session.commit()
    return json.dumps({'success': True, 'data': task.serialize()}), 200

@app.route('/task/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found!'}), 404
    db.session.delete(task)
    db.session.commit()
    return json.dumps({'success': True, 'data': task.serialize()}), 200

@app.route('/task/<int:task_id>/subtasks/', methods=['POST'])
def create_subtask(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found!'}), 404
    post_body = json.loads(request.data)
    subtask = Subtask(
        description=post_body.get('description'),
        done=bool(post_body.get('done')),
        task_id=task.id,
    )
    task.subtasks.append(subtask)
    db.session.add(subtask)
    db.session.commit()
    return json.dumps({'success': True, 'data': subtask.serialize()})

@app.route('/task/<int:task_id>/category/', methods=['POST'])
def assign_category(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found!'}), 404
    post_body = json.loads(request.data)
    category = Category.query.filter_by(description=post_body.get('description', '')).first()
    if not category:
        category = Category(
            description=post_body.get('description', ''),
            color=post_body.get('color')
        )
    task.categories.append(category)
    db.session.commit()
    return json.dumps({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
