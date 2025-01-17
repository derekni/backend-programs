from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table_student = db.Table('association_student', db.Model.metadata, 
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

association_table_teacher = db.Table('association_teacher', db.Model.metadata, 
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', cascade='delete')
    teachers = db.relationship('User', secondary=association_table_teacher, back_populates='courses_t')
    students = db.relationship('User', secondary=association_table_student, back_populates='courses_s')

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', '')
        self.name = kwargs.get('name', '')
        self.assignments = []
    
    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name
        }

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.due_date = kwargs.get('due_date', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses_t = db.relationship('Course', secondary=association_table_teacher, back_populates='teachers')
    courses_s = db.relationship('Course', secondary=association_table_student, back_populates='students')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid
        }