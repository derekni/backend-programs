from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bathroom(db.Model):
    __tablename__ = 'bathroom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    #latitude = db.Column(db.Numeric(8,6), nullable=False)
    #longitude = db.Column(db.Numeric(9,6), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.latitude = kwargs.get('latitude', '')
        self.longitude = kwargs.get('longitude', '')
        self.rating = kwargs.get('rating', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'rating': self.rating
        }
