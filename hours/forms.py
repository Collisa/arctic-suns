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

class MonthForm(FlaskForm):
    year_id = SelectField("Jaar", choices=[2020])
    month_id = SelectField("Maand", choices=[(1, 'Januari'), (2, 'Februari'), (3, 'Maart'), (4, 'April'), (5, 'Mei'), (6, 'Juni'), (7, 'Juli'), (8, 'Augustus'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December')])
    