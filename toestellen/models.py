from app import db
from sqla_softdelete import SoftDeleteMixin


class ArcticSun(db.Model, SoftDeleteMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    date_in = db.Column(db.Date)
    date_out = db.Column(db.Date)
    pick_up_location = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    status = db.Column(db.String(15))
    remarks = db.Column(db.Text)
    type = db.Column(db.String(25))