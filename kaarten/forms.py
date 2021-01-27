from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, SelectField


class CardForm(FlaskForm):
    chauffeur = StringField("Chauffeur")
    date_out = DateField("Meegegeven")
    date_retour = DateField("Retour")
    card = SelectField(
        "Kaart",
        choices=[
            "Shell XL",
            "Shell MB",
            "Shell S",
            "Total Arie",
            "Total Kris",
            "Total 4",
            "Total 5",
            "Dats Kris",
            "Dats Jochen",
            "Dats Lisa",
        ],
    )
    submit = SubmitField("Toevoegen")
