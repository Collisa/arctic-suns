from flask import render_template, request, redirect, url_for, flash
from app import app, db
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
import calendar
from hours.forms import HoursForm, PersonForm, MonthForm, WorkerForm
from hours.models import Employee, Worker
from hours.extrahours_calculation import (
    calculate_extrahours_week,
    calculate_extrahours_month,
    calculate_extrahours_year,
    calculate_month_view,
    hours_in_hours_and_minutes,
)
from hours.weekly_view import get_weekly_view_days
import locale
import copy
from dateutil.relativedelta import relativedelta

weekDays = (
    "Maandag",
    "Dinsdag",
    "Woensdag",
    "Donderdag",
    "Vrijdag",
    "Zaterdag",
    "Zondag",
)

werkuren = True


@app.route("/hours", methods=["GET"])
@login_required
def hours_index():
    if current_user.firm == "Collibri":

        year, month = calculate_month_view()
        locale.setlocale(locale.LC_ALL, "nl_NL")
        # month_view = calendar.month(year, month)
        month_view = calendar.TextCalendar().formatmonth(year, month)

        person_id = request.args.get("person_id", "1")
        hours_off = (
            Worker.query.filter(Worker.id == person_id).first().total_hours_off_a_year
        )
        # totaal op te nemen uren
        days_off = round(
            hours_off
            / Worker.query.filter(Worker.id == person_id)
            .first()
            .total_hours_in_one_full_workday,
            2,
        )

        extrahours_year, leave_days, leave_extra_minutes = calculate_extrahours_year(
            person_id
        )
        # leave_hours zonder combi-dagen
        leave_hours = (
            leave_days
            * Worker.query.filter(Worker.id == person_id)
            .first()
            .total_hours_in_one_full_workday
        )
        leave_hours -= ((leave_extra_minutes / 60) / 8) * Worker.query.filter(
            Worker.id == person_id
        ).first().total_hours_in_one_full_workday

        leave_hours = round(leave_hours, 2)

        # opgenomen uren
        leave_days_off = round(
            leave_hours
            / Worker.query.filter(Worker.id == person_id)
            .first()
            .total_hours_in_one_full_workday,
            2,
        )

        extra_hours_year, extraminutes_year = hours_in_hours_and_minutes(
            extrahours_year
        )
        extrahours_month, extraminutes_month = hours_in_hours_and_minutes(
            calculate_extrahours_month(person_id)
        )
        extrahours_week, extraminutes_week = hours_in_hours_and_minutes(
            calculate_extrahours_week(person_id)
        )
        print(leave_extra_minutes)
        data = {
            "extrahours_week": extrahours_week,
            "extrahours_month": extrahours_month,
            "extrahours_year": extra_hours_year,
            "extraminutes_year": extraminutes_year,
            "extraminutes_month": extraminutes_month,
            "extraminutes_week": extraminutes_week,
            "leave_hours": leave_hours,
            "weeklyview_days": get_weekly_view_days(person_id),
            "month": month,
            "year": year,
            "days_off": days_off,
            "leave_days_off": leave_days_off,
        }

        return render_template(
            "hours/index.html",
            hours_off=hours_off,
            template_form=HoursForm(),
            person_form=PersonForm(person_id=person_id),
            person_id=person_id,
            data=data,
            month_view=month_view,
            current_user=current_user,
            werkuren=werkuren,
        )


@app.route("/hours/add", methods=["POST"])
@login_required
def hours_add():
    if current_user.firm == "Collibri" and current_user.function == "admin":
        hour_form = HoursForm(request.form)

        extra_hours = 0

        if hour_form.end_hour.data:
            extra_hours = datetime.combine(
                date.today(), hour_form.end_hour.data
            ) - datetime.combine(date.today(), hour_form.start_hour.data)
            extra_hours = extra_hours - timedelta(hours=8)
            extra_hours = int(extra_hours.total_seconds() / 60)

        try:
            day = Employee(
                person_id=hour_form.person_id.data,
                workday=hour_form.workday.data,
                start_hour=hour_form.start_hour.data,
                end_hour=hour_form.end_hour.data,
                type_day=hour_form.type_day.data,
                total_leave_days=1 if hour_form.type_day.data == "verlof" else 0,
                extra_hours=extra_hours,
            )
            db.session.add(day)
            db.session.commit()

        except IntegrityError:
            return redirect(
                url_for(
                    "hours_edit",
                    datum=day.workday,
                    id=day.person_id,
                    type_day=day.type_day,
                    start_hour=day.start_hour,
                    end_hour=day.end_hour,
                )
            )

        return redirect(url_for("hours_index", person_id=day.person_id))


@app.route("/hours/edit/<int:id>/<datum>/", methods=["GET", "POST"])
@login_required
def hours_edit(id, datum):
    if current_user.firm == "Collibri" and current_user.function == "admin":
        item_to_change = Employee.query.filter(
            Employee.person_id == id, Employee.workday == datum
        ).first()

        extra_hours = 0

        if request.method == "POST":
            form = HoursForm(request.form)

            if form.end_hour.data:
                extra_hours = datetime.combine(
                    date.today(), form.end_hour.data
                ) - datetime.combine(date.today(), form.start_hour.data)
                extra_hours = extra_hours - timedelta(hours=8)
                extra_hours = int(extra_hours.total_seconds() / 60)

            item_to_change.person_id = id
            item_to_change.workday = form.workday.data
            item_to_change.start_hour = form.start_hour.data
            item_to_change.end_hour = form.end_hour.data
            item_to_change.type_day = form.type_day.data
            item_to_change.total_leave_days = 1 if form.type_day.data == "verlof" else 0
            item_to_change.extra_hours = extra_hours

            db.session.commit()

            return redirect(url_for("hours_index", person_id=id))

        item_to_change2 = copy.deepcopy(item_to_change)
        if request.args.get("start_hour"):
            item_to_change2.start_hour = datetime.strptime(
                request.args.get("start_hour"), "%H:%M:%S"
            )

        if request.args.get("end_hour"):
            item_to_change2.end_hour = datetime.strptime(
                request.args.get("end_hour"), "%H:%M:%S"
            )

        item_to_change2.type_day = request.args.get("type_day")

        return render_template(
            "hours/edit.html",
            template_form=HoursForm(obj=item_to_change2),
            item_to_change=item_to_change,
            id=id,
            datum=datum,
            current_user=current_user,
        )


@app.route("/hours/month/<int:id>")
@login_required
def month_view(id):
    if current_user.firm == "Collibri":
        year_id = int(request.args.get("year_id"))
        month_id = int(request.args.get("month_id"))

        firstdayofmonth = datetime.today().replace(
            year=year_id, month=month_id, day=1
        ) - timedelta(days=1)

        lastdayofmonth = (
            firstdayofmonth.replace(day=1)
            + relativedelta(months=+2)
            - timedelta(days=1)
        )

        qry = Employee.query.filter(
            Employee.person_id == id,
            Employee.workday.between(firstdayofmonth, lastdayofmonth),
        ).order_by(Employee.workday.asc())

        return render_template(
            "hours/month-view.html",
            id=id,
            qry=qry,
            weekDays=weekDays,
            current_user=current_user,
            month_form=MonthForm(year_id=year_id, month_id=month_id),
            year_id=year_id,
            month_id=month_id,
            werkuren=werkuren,
            abs=abs,
        )


@app.route("/hours/worker_settings")
@login_required
def worker_settings():
    if current_user.firm == "Collibri" and current_user.function == "admin":
        workers = Worker.query.all()
        return render_template(
            "hours/worker-settings.html", form=WorkerForm(), workers=workers
        )


@app.route("/hours/add_worker", methods=["POST"])
@login_required
def add_worker():
    if current_user.firm == "Collibri" and current_user.function == "admin":
        form = WorkerForm(request.form)
        if form.validate():
            worker = Worker(
                name=form.name.data,
                total_hours_off_a_year=form.total_hours_off_a_year.data,
                total_hours_in_one_full_workday=form.total_hours_in_one_full_workday.data,
                extra_minutes_left_from_last_year=form.extra_minutes_left_from_last_year.data,
            )
            db.session.add(worker)
            db.session.commit()
        else:
            if form.errors:
                flash("Je kan enkel een . gebruiken, geen ,!")
    return redirect(url_for("hours_index"))
