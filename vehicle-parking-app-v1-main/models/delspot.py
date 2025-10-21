from . import db
class Dels(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    spot_id=db.Column(db.Integer,nullable=False)