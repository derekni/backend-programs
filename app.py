import json
from db import db, Task
from flask import Flask, request

app = Flask(__name__)

db_filename = "todo.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
	db.create_all()

@app.route('/')
@app.route('/tasks/')
def get_tasks():
	tasks = Task.query.all()
	res = {'success': True, 'data': [t.serialize() for t in tasks]}
	return json.dumps(res), 200

@app.route('/tasks/', methods=['POST'])
def create_task():
	post_body = json.loads(request.data)
	description = post_body.get('description','')
	task = Task(
		description=description,
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
	return json.dumps({'success': True, 'data': task}), 200

@app.route('/task/<int:task_id>/', methods=['POST'])
def update_task(task_id):
	post_body = json.loads(request.data)
	task = Task.query.filter_by(id=task_id).first()
	description = post_Body.get('description', task.description)
	done = post_body.get('done', task.done)
	task.description = description
	task.done = done
	db.session.commit()
	if not task:
		return json.dumps({'success': False, 'error': 'Task not found!'}), 404
	return json.dumps({'success': True, 'data': task}), 200

@app.route('/task/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
	task = Task.query.filter_by(id=task_id).first()
	if not task:
		return json.dumps({'success': False, 'error': 'Task not found!'}), 404
	description = post_Body.get('description', task.description)
	done = post_body.get('done', task.done)
	task.description = description
	task.done = done
	db.session.commit()
	if not task:
		return json.dumps({'success': False, 'error': 'Task not found!'}), 404
	return json.dumps({'success': True, 'data': task}), 200

@app.route('/task/<int:task_id>/subtasks/', methods=['POST'])
def create_subtask(task_id):
	task = Task.query.filter_by(id=task_id).first()
	if not task:
		return json.dumps({'success': False, 'error': 'Task not found!'}), 404
	post_body = json.loads(request.data)
	subtask = Subtask(
		description = post_body.get('description', ''),
		done = post_body.get('done', False),
		task_id = task_id
	)
	task.subtasks.append(subtask)
	db.session.add(subtask)
	db.session.commit()
	return json.dumps({'success': True, 'data': subtask.serialize()}), 200

@app.route('/task/<int:task_id>/category/', methods=['POST'])
def create_category(task_id):
	task = Task.query.filter_by(id=task_id).first()
	if not task:
		return json.dumps({'success': False, 'error': 'Task not found!'}), 404
	post_body = json.loads(request.data)
	category = Category.query.filter_by(description=post_body.get('description')).first()
	if not category:
		category = Category(
			description = post_body.get('description', ''),
			color = post_body.get('color')
		)
	task.categories.append(category)
	db.session.add(category)
	db.session.commit()
	return json.dumps({'success': True, 'data': category.serialize()}), 200
	
'''
@app.route('/task/<int:task_id>/subtasks/')
def get_subtasks_of_task(task_id):
	res = {'success': True, 'data': Db.get_subtasks_of_task(task_id)}
	return json.dumps(res), 200

@app.route('/subtasks/')
def get_subtasks():
	res = {'success': True, 'data': Db.get_all_subtasks()}
	return json.dumps(res), 200

@app.route('/tasks/<int:task_id>/', methods=['POST'])
def update_task(task_id):
	task = Db.get_task_by_id(task_id)
	if task is not None:
		post_body = json.loads(request.data)
		task['description'] = post_body['description']
		task['done'] = post_body['done']
		return json.dumps({'success': True, 'data': task}), 200
	return json.dumps({'success': False, 'error': 'Task not found!'}), 404

@app.route('/tasks/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
	if task_id in tasks:
		task = tasks[task_id]
		del tasks[task_id]
		return json.dumps({'success': True, 'data': task}), 200
	return json.dumps({'success': False, 'error': 'Task not found!'}), 404
'''
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)