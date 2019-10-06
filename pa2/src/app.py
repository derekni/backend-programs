import json
import db
from flask import Flask, request

app = Flask(__name__)

Db = db.DB()

@app.route('/')
@app.route('/api/users/')
def get_users():
	res = {'success': True, 'data': Db.get_all_users()}
	return json.dumps(res), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body['name']
    username = post_body['username']
    user = {
		'id': Db.create_user(name, username),
		'name': name,
		'username': username,
        'balance': 0
	}
    return json.dumps({'success': True, 'data': user}), 201

@app.route('/api/user/<int:id>/')
def get_user(id):
	user = Db.get_user_by_id(id)
	if user is not None:
		return json.dumps({'success': True, 'data': user}), 200
	return json.dumps({'success': False, 'error': 'User not found!'}), 404

@app.route('/api/user/<int:id>/', methods=['DELETE'])
def delete_user(id):
	user = Db.delete_user_by_id(id)
	if user is not None:
		return json.dumps({'success': True, 'data': user}), 200
	return json.dumps({'success': False, 'error': 'User not found!'}), 404

@app.route('/api/send/', methods=['POST'])
def send():
    post_body = json.loads(request.data)
    sender_id = post_body['sender_id']
    receiver_id = post_body['receiver_id']
    amount = post_body['amount']
    if Db.send_money(sender_id, receiver_id, amount):
        return json.dumps({'success': True, 'data': {'sender_id': sender_id, 'receiver_id': receiver_id, 'amount': amount}})
    return json.dumps({'success': False, 'error': 'Not enough money to send!'}), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)