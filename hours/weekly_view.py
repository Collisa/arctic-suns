from datetime import datetime, timedelta
from hours.models import Employee


def get_weekly_view_days(person_id):
    firstdayofweek = datetime.today() - timedelta(
        days=(datetime.today().weekday() % 7) + 1
    )
    lastdayofweek = datetime.today() + timedelta(
        days=6 - (datetime.today().weekday() % 7)
    )

    result = {}
    qry = Employee.query.filter(
        Employee.person_id == person_id,
        Employee.workday.between(firstdayofweek, lastdayofweek),
    )

    for row in qry:
        weekday = row.workday.weekday()

        if row.type_day == "werkdag":
            result[weekday] = {
                "type": "werkdag",
                "start": row.start_hour,
                "end": row.end_hour,
            }
        elif row.type_day == "recupdag":
            result[weekday] = {"type": "recupdag"}
        elif row.type_day == "verlof":
            result[weekday] = {"type": "verlof"}
        elif row.type_day == "weekend":
            result[weekday] = {"type": "weekend"}
        elif row.type_day == "feestdag":
            result[weekday] = {"type": "feestdag"}
        elif row.type_day == "technisch werkloos":
            result[weekday] = {"type": "TW"}
        elif (
            row.type_day
            == "combinatie werkdag + verlofuren (enkel de gewerkte uren in te vullen)"
        ):
            result[weekday] = {
                "type": "combi",
                "start": row.start_hour,
                "end": row.end_hour,
            }

    return result
