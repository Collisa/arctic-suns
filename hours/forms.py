from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    FloatField,
    validators,
    IntegerField,
)
from wtforms_components import TimeField

from hours.models import Worker

workers = []
for worker in Worker.query.all():
    workers.append((worker.id, worker.name))

# employees = [(1, "Lisa"), (2, "Elio")]
employees = workers


class HoursForm(FlaskForm):
    # person_name = SelectField("Werknemer", choices=["Lisa", "Elio"])
    person_id = StringField("")
    workday = DateField("Werkdag")
    start_hour = TimeField("Start")
    end_hour = TimeField("Eind")
    type_day = SelectField(
        "Type dag",
        choices=[
            "werkdag",
            "weekend",
            "verlof",
            "feestdag",
            "recupdag",
            "technisch werkloos",
            "combinatie werkdag + verlofuren (enkel de gewerkte uren in te vullen)",
        ],
    )
    submit = SubmitField("Toevoegen")


class PersonForm(FlaskForm):
    person_id = SelectField("Werknemer", choices=employees)


class WorkerForm(FlaskForm):
    name = StringField("Naam")
    total_hours_off_a_year = FloatField(
        "Totaal uren verlof per jaar", [validators.InputRequired()]
    )
    total_hours_in_one_full_workday = FloatField(
        "Uren in 1 werkdag", [validators.InputRequired()]
    )
    extra_minutes_left_from_last_year = IntegerField(
        "Overuren mee te nemen van vorig jaar (in minuten)"
    )
    submit = SubmitField("Voeg toe")


class MonthForm(FlaskForm):
    year_id = SelectField("Jaar", choices=[2020, 2021, 2022])
    month_id = SelectField(
        "Maand",
        choices=[
            (1, "Januari"),
            (2, "Februari"),
            (3, "Maart"),
            (4, "April"),
            (5, "Mei"),
            (6, "Juni"),
            (7, "Juli"),
            (8, "Augustus"),
            (9, "September"),
            (10, "Oktober"),
            (11, "November"),
            (12, "December"),
        ],
    )
