from datetime import date, datetime, timedelta
from hours.models import Employee
from models import ArcticSun
from app import db
import calendar


def calculate_extrahours_week(employee_id):
    extra_hours = 0
    firstdayofweek = datetime.today(
    ) - timedelta(days=(datetime.today().weekday() % 7) + 1)

    lastdayofweek = datetime.today(
    ) + timedelta(days=6 - (datetime.today().weekday() % 7))

    qry = Employee.query.filter(Employee.person_id == employee_id,
                                Employee.workday.between(firstdayofweek, lastdayofweek), Employee.type_day.in_(['werkdag', 'recupdag']))

    for row in qry:
        if row.type_day == 'werkdag':
            extra_hours += row.extra_hours
        elif row.type_day == 'recupdag':
            extra_hours -= 8 * 60

    extra_hours = extra_hours / 60
    return round(extra_hours, 2)


def calculate_extrahours_month(employee_id):
    extra_hours = 0

    firstdayofmonth = datetime.today().replace(day=1) - timedelta(days=1)


    lastdayofmonth = (datetime.today().replace(
        month=firstdayofmonth.month + 1) - timedelta(days=1))

    qry = Employee.query.filter(Employee.person_id == employee_id,
                                Employee.workday.between(firstdayofmonth, lastdayofmonth), Employee.type_day.in_(['werkdag', 'recupdag']))

    for row in qry:
        if row.type_day == 'werkdag':
            extra_hours += row.extra_hours
        elif row.type_day == 'recupdag':
            extra_hours -= 8 * 60

    extra_hours = extra_hours / 60
    return round(extra_hours, 2)


def calculate_extrahours_year(employee_id):
    extra_hours = 0
    leave_days = 0

    firstdayofyear = datetime.today().replace(month=1, day=1) - timedelta(days=1)


    lastdayofyear = datetime.today().replace(month=12, day=31)

    qry = Employee.query.filter(Employee.person_id == employee_id,
                                Employee.workday.between(firstdayofyear, lastdayofyear), Employee.type_day.in_(['werkdag', 'verlof', 'recupdag']))

    for row in qry:
        if row.type_day == 'werkdag':
            extra_hours += row.extra_hours
        elif row.type_day == 'verlof':
            leave_days += 1
        elif row.type_day == 'recupdag':
            extra_hours -= 8 * 60

    extra_hours = extra_hours / 60
    return round(extra_hours, 2), leave_days


def calculate_month_view():
    year = datetime.now().year
    month = datetime.now().month
    return year, month
