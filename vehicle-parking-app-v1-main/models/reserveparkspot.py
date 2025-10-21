from . import db
from datetime import datetime

class ReserveParkSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots1.id'), nullable=False)
    spot_id = db.Column(db.Integer, nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    Action= db.Column(db.String(50), nullable=False, default='Release')
