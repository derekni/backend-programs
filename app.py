import json
import db
from flask import Flask, request

app = Flask(__name__)

Db = db.DB()

@app.route('/')
@app.route('/tasks/')
def get_tasks():
	res = {'success': True, 'data': Db.get_all_tasks()}
	return json.dumps(res), 200

@app.route('/tasks/', methods=['POST'])
def create_task():
	post_body = json.loads(request.data)
	description = post_body['description']
	task = {
		'id': Db.insert_task(description, False),
		'description': description,
		'done': False
	}
	return json.dumps({'success': True, 'data': task}), 201

@app.route('/tasks/<int:task_id>/')
def get_task(task_id):
	task = Db.get_task_by_id(task_id)
	if task is not None:
		return json.dumps({'success': True, 'data': task}), 200
	return json.dumps({'success': False, 'error': 'Task not found!'}), 404
'''
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