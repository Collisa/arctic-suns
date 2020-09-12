from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from flask_login import login_required
from datetime import datetime, date, timedelta
import calendar
from hours.forms import HoursForm, PersonForm
from hours.models import Employee

total_leave_days = 0

@app.route('/hours', methods=["GET"])
@login_required
def hours_index():
    days_off = 21
    month_view = calendar.month(2020, 8)
    all_employees = Employee.query.all()
    person_id = request.args.get('person_id', '1')
    return render_template("hours/index.html", days_off=days_off, month_view=month_view, template_form=HoursForm(), person_form=PersonForm(person_id=person_id), all_employees=all_employees, person_id=person_id)


# employees = [{id: 1, name: "Lisa"}, {id: 2, name: "Elio"}]


@app.route('/hours/add', methods=["POST"])
@login_required
def hours_add():
    hour_form = HoursForm(request.form)

    extra_hours = None

    if hour_form.end_hour.data:
        extra_hours = datetime.combine(date.today(), hour_form.end_hour.data) - datetime.combine(date.today(), hour_form.start_hour.data)
        extra_hours = extra_hours - timedelta(hours=8)

    day = Employee(
        person_id=hour_form.person_id.data,
        workday=hour_form.workday.data,
        start_hour=hour_form.start_hour.data,
        end_hour=hour_form.end_hour.data,
        type_day=hour_form.type_day.data,
        total_leave_days=total_leave_days + 1 if hour_form.type_day.data =="verlof" else total_leave_days,
        extra_hours=str(extra_hours))
    db.session.add(day)
    db.session.commit()

    return redirect(url_for('hours_index'))
