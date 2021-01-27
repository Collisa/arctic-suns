from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class Input(FlaskForm):
    name = StringField("Identificatie")
    date_in = DateField("Afhaling")
    date_out = DateField("Levering")
    pick_up_location = TextAreaField("Afhaallocatie")
    destination = TextAreaField("Leverlocatie")
    status = SelectField(
        "Status", choices=["", "Gerepareerd", "Loaner", "Defect", "Nieuw", "Onbekend"]
    )
    submit = SubmitField("Toevoegen")
    remarks = TextAreaField("Opmerkingen")
    type = StringField("")
