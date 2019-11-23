import json
from db import db, Bathroom
from flask import Flask, request
import os

# define db filename
db_filename = "bathrooms.db"
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

@app.route('/bathrooms/')
def get_bathrooms():
    bathrooms = Bathroom.query.all()
    res = {'success': True, 'data': [bathroom.serialize() for bathroom in bathrooms]}
    return json.dumps(res), 200

@app.route('/bathrooms/', methods=['POST'])
def create_bathroom():
    post_body = json.loads(request.data)
    bathroom = Bathroom(
        name=post_body.get('name'),
        description=post_body.get('description'),
        latitude=post_body.get('latitude'),
        longitude=post_body.get('longitude'),
        rating=post_body.get('rating')
    )
    db.session.add(bathroom)
    db.session.commit()
    return json.dumps({'success': True, 'data': bathroom.serialize()}), 201

@app.route('/bathroom/<int:bathroom_id>/')
def get_bathroom(bathroom_id):
    bathroom = Bathroom.query.filter_by(id=bathroom_id).first()
    if not bathroom:
        return json.dumps({'success': False, 'error': 'Bathroom not found!'}), 404
    return json.dumps({'success': True, 'data': bathroom.serialize()}), 200
    
@app.route('/bathroom/<int:bathroom_id>/', methods=['POST'])
def update_bathroom(bathroom_id):
    bathroom = Bathroom.query.filter_by(id=bathroom_id).first()
    if not bathroom:
        return json.dumps({'success': False, 'error': 'Bathroom not found!'}), 404
    post_body = json.loads(request.data)
    bathroom.name = post_body.get('name', bathroom.name)
    bathroom.description = post_body.get('description', bathroom.description)
    bathroom.latitude = post_body.get('latitude', bathroom.latitude)
    bathroom.longitude = post_body.get('longitude', bathroom.longitude)
    bathroom.rating = post_body.get('rating', bathroom.rating)
    db.session.commit()
    return json.dumps({'success': True, 'data': bathroom.serialize()}), 200

@app.route('/bathroom/<int:bathroom_id>/', methods=['DELETE'])
def delete_bathroom(bathroom_id):
    bathroom = Bathroom.query.filter_by(id=bathroom_id).first()
    if not bathroom:
        return json.dumps({'success': False, 'error': 'Bathroom not found!'}), 404
    db.session.delete(bathroom)
    db.session.commit()
    return json.dumps({'success': True, 'data': bathroom.serialize()}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
