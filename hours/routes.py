from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from flask_login import login_required, current_user
from authentication.models import User
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
import calendar
from hours.forms import HoursForm, PersonForm
from hours.models import Employee
from hours.extrahours_calculation import calculate_extrahours_week, calculate_extrahours_month, calculate_extrahours_year, calculate_month_view
from hours.weekly_view import get_weekly_view_days
import locale
import copy
from dateutil.relativedelta import relativedelta

weekDays = ("Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag")



@app.route('/hours', methods=["GET"])
@login_required
def hours_index():
    days_off = 21
    
    year, month = calculate_month_view()
    locale.setlocale(locale.LC_ALL, 'nl_NL')
    # month_view = calendar.month(year, month)
    month_view = calendar.TextCalendar().formatmonth(year, month)

    person_id = request.args.get('person_id', '1')

    extrahours_year, leavedays = calculate_extrahours_year(person_id)
    
    data = {
        'extrahours_week': calculate_extrahours_week(person_id),
        'extrahours_month': calculate_extrahours_month(person_id),
        'extrahours_year': extrahours_year,
        'leavedays': leavedays,
        'weeklyview_days': get_weekly_view_days(person_id),
        'month': month
    }

    return render_template("hours/index.html", days_off=days_off, template_form=HoursForm(), person_form=PersonForm(person_id=person_id), person_id=person_id, data=data, month_view=month_view, current_user=current_user)



@app.route('/hours/add', methods=["POST"])
@login_required
def hours_add():
    hour_form = HoursForm(request.form)
    
    extra_hours = 0

    if hour_form.end_hour.data:
        extra_hours = datetime.combine(date.today(), hour_form.end_hour.data) - datetime.combine(date.today(), hour_form.start_hour.data)
        extra_hours = extra_hours - timedelta(hours=8)
        extra_hours = int(extra_hours.total_seconds() / 60)

    try:
        day = Employee(
            person_id=hour_form.person_id.data,
            workday=hour_form.workday.data,
            start_hour=hour_form.start_hour.data,
            end_hour=hour_form.end_hour.data,
            type_day=hour_form.type_day.data,
            total_leave_days= 1 if hour_form.type_day.data == "verlof" else 0,
            extra_hours=extra_hours)
        db.session.add(day)
        db.session.commit()
    
    except IntegrityError:
        return redirect(url_for('hours_edit', datum=day.workday, id=day.person_id, type_day=day.type_day, start_hour=day.start_hour, end_hour=day.end_hour))

    return redirect(url_for('hours_index', person_id=day.person_id))

@app.route('/hours/edit/<int:id>/<datum>/', methods=["GET", "POST"])
@login_required
def hours_edit(id, datum):
    item_to_change = Employee.query.filter(Employee.person_id == id, Employee.workday == datum).first()

    extra_hours = 0

    if request.method == "POST":
        form = HoursForm(request.form)
        
        if form.end_hour.data:
            
            extra_hours = datetime.combine(date.today(), form.end_hour.data) - datetime.combine(date.today(), form.start_hour.data)
            extra_hours = extra_hours - timedelta(hours=8)
            extra_hours = int(extra_hours.total_seconds() / 60) 

        item_to_change.person_id=id
        item_to_change.workday=form.workday.data
        item_to_change.start_hour=form.start_hour.data
        item_to_change.end_hour=form.end_hour.data
        item_to_change.type_day=form.type_day.data
        item_to_change.total_leave_days=1 if form.type_day.data == "verlof" else 0
        item_to_change.extra_hours=extra_hours

        db.session.commit()

        return redirect(url_for('hours_index', person_id=id))


    item_to_change2 = copy.deepcopy(item_to_change)
    if(request.args.get('start_hour')):
        item_to_change2.start_hour=datetime.strptime(request.args.get('start_hour'), '%H:%M:%S')

    if(request.args.get('end_hour')):
        item_to_change2.end_hour=datetime.strptime(request.args.get('end_hour'), '%H:%M:%S')
    
    item_to_change2.type_day=request.args.get('type_day')

    return render_template('hours/edit.html', template_form=HoursForm(obj=item_to_change2), item_to_change=item_to_change, id=id, datum=datum, current_user=current_user)


@app.route('/hours/month/<int:id>/<int:month>')
@login_required
def month_view(id, month):
    firstdayofmonth = datetime.today().replace(month=month, day=1) - timedelta(days=1)

    lastdayofmonth = (firstdayofmonth.replace(day=1) + relativedelta(months=+2) - timedelta(days=1))

    qry = Employee.query.filter(Employee.person_id == id,
                                Employee.workday.between(firstdayofmonth, lastdayofmonth)).order_by(Employee.workday.asc())

    return render_template('hours/month-view.html', id=id, qry=qry, weekDays=weekDays, current_user=current_user)


