from . import db
class Lots1(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    prime_location=db.Column(db.String(50), nullable=False)
    price=db.Column(db.Integer, nullable=False)
    status=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(100), nullable=False)
    pin_code=db.Column(db.String(10), nullable=False)
    max_slots=db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(50), nullable=False)