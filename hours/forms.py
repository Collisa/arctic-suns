from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms_components import TimeField


employees = [(1, "Lisa"), (2, "Elio")]


class HoursForm(FlaskForm):
    # person_name = SelectField("Werknemer", choices=["Lisa", "Elio"])
    person_id = StringField("")
    workday = DateField("Werkdag")
    start_hour = TimeField("Start")
    end_hour = TimeField("Eind")
    type_day = SelectField("Type dag", choices=["werkdag", "weekend", "verlof", "feestdag", "recupdag", "technisch werkloos"])
    submit = SubmitField("Toevoegen")


class PersonForm(FlaskForm):
    person_id = SelectField("Werknemer", choices=employees)