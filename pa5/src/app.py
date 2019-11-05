import json
from db import db, Course, Assignment, User
from flask import Flask, request

app = Flask(__name__)

db_filename = "courses.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/api/courses/')
def get_courses():
    courses = Course.query.all()
    res = {'success': True, 'data': [c.serialize() for c in courses]}
    return json.dumps(res), 200

@app.route('/api/courses/', methods=['POST'])
def create_course():
    post_body = json.loads(request.data)
    code = post_body.get('code', '')
    name = post_body.get('name', '')
    course = Course(
        code=code, 
        name=name
    )
    db.session.add(course)
    db.session.commit()
    data = course.serialize()
    data['assignments'] = [a.serialize() for a in course.assignments]
    data['instructors'] = [t.serialize() for t in course.teachers]
    data['students'] = [s.serialize() for s in course.students]
    return json.dumps({'success': True, 'data': data}), 201

@app.route('/api/course/<int:course_id>/')
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    data = course.serialize()
    data['assignments'] = [a.serialize() for a in course.assignments]
    data['instructors'] = [t.serialize() for t in course.teachers]
    data['students'] = [s.serialize() for s in course.students]
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    netid = post_body.get('netid', '')
    user = User(
        name=name,
        netid=netid
    )
    db.session.add(user)
    db.session.commit()
    data = user.serialize()
    data['courses'] = [c.serialize() for c in user.courses_t] + [c.serialize() for c in user.courses_s]
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    data = user.serialize()
    data['courses'] = [c.serialize() for c in user.courses_t] + [c.serialize() for c in user.courses_s]
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/course/<int:course_id>/add/', methods=['POST'])
def add_user(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    post_body = json.loads(request.data)
    user_type = post_body.get('type', '')
    user_id = post_body.get('user_id', '')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    if user_type == 'student':
	    course.students.append(user)
    else:
        course.teachers.append(user)
    db.session.add(user)
    db.session.commit()
    data = course.serialize()
    data['assignments'] = [a.serialize() for a in course.assignments]
    data['instructors'] = [t.serialize() for t in course.teachers]
    data['students'] = [s.serialize() for s in course.students]
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/course/<int:course_id>/assignment/', methods=['POST'])
def create_assignment(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    post_body = json.loads(request.data)
    title = post_body.get('title', '')
    due_date = post_body.get('due_date', '')
    assignment = Assignment(
        title=title,
        due_date=due_date
    )
    course.assignments.append(assignment)
    db.session.add(assignment)
    db.session.commit()
    data = assignment.serialize()
    data['course'] = course.serialize()
    return json.dumps({'success': True, 'data': data}), 200
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)