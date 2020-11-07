from datetime import datetime
from app import db
from sqla_softdelete import SoftDeleteMixin

class Card(db.Model, SoftDeleteMixin):
    id = db.Column(db.Integer, primary_key = True)
    card = db.Column(db.String(25))
    date_out = db.Column(db.Date)
    date_retour = db.Column(db.Date)
    chauffeur = db.Column(db.String(50))