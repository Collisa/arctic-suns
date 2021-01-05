from datetime import datetime, timedelta
from hours.models import Employee, Worker
import math


def hours_in_hours_and_minutes(extra_hours):
    hours = math.trunc(extra_hours)
    minutes = round((extra_hours * 60) - (hours * 60))
    return hours, minutes


def calculate_extrahours_week(employee_id):
    extra_hours = 0
    firstdayofweek = datetime.today() - timedelta(
        days=(datetime.today().weekday() % 7) + 1
    )

    lastdayofweek = datetime.today() + timedelta(
        days=6 - (datetime.today().weekday() % 7)
    )

    qry = Employee.query.filter(
        Employee.person_id == employee_id,
        Employee.workday.between(firstdayofweek, lastdayofweek),
        Employee.type_day.in_(["werkdag", "recupdag"]),
    )

    for row in qry:
        if row.type_day == "werkdag":
            extra_hours += row.extra_hours
        elif row.type_day == "recupdag":
            extra_hours -= 8 * 60

    extra_hours = extra_hours / 60
    return round(extra_hours, 2)


def calculate_extrahours_month(employee_id):

    firstdayofmonth = datetime.today().replace(day=1) - timedelta(days=1)

    if (firstdayofmonth.month + 1) == 13:
        month = 1
    else:
        month = firstdayofmonth.month + 1

    lastdayofmonth = datetime.today().replace(month=month) - timedelta(days=1)

    qry = Employee.query.filter(
        Employee.person_id == employee_id,
        Employee.workday.between(firstdayofmonth, lastdayofmonth),
        Employee.type_day.in_(["werkdag", "recupdag"]),
    )
    extra_hours = 0
    for row in qry:
        if row.type_day == "werkdag":
            extra_hours += row.extra_hours
        elif row.type_day == "recupdag":
            extra_hours -= 8 * 60

    extra_hours = extra_hours / 60
    return round(extra_hours, 2)


def calculate_extrahours_year(employee_id):
    extra_hours = 0
    leave_days = 0
    leave_extra_minutes = 0

    firstdayofyear = datetime.today().replace(month=1, day=1) - timedelta(days=1)

    lastdayofyear = datetime.today().replace(month=12, day=31)

    qry = Employee.query.filter(
        Employee.person_id == employee_id,
        Employee.workday.between(firstdayofyear, lastdayofyear),
        Employee.type_day.in_(
            [
                "werkdag",
                "verlof",
                "recupdag",
                "combinatie werkdag + verlofuren (enkel de gewerkte uren in te vullen)",
            ]
        ),
    )

    for row in qry:
        if row.type_day == "werkdag":
            extra_hours += row.extra_hours
        elif row.type_day == "verlof":
            leave_days += 1
        elif row.type_day == "recupdag":
            extra_hours -= 8 * 60
        elif (
            row.type_day
            == "combinatie werkdag + verlofuren (enkel de gewerkte uren in te vullen)"
        ):
            leave_extra_minutes += row.extra_hours

    extra_hours_last_year = (
        Worker.query.filter(Worker.id == employee_id)
        .first()
        .extra_minutes_left_from_last_year
    )

    extra_hours = (extra_hours + extra_hours_last_year) / 60
    return round(extra_hours, 2), leave_days, leave_extra_minutes


def calculate_month_view():
    year = datetime.now().year
    month = datetime.now().month
    return year, month
