from app import db


class Employee(db.Model):  # chose name wrong, kept it like this
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, nullable=False)
    workday = db.Column(db.Date)
    start_hour = db.Column(db.Time)
    end_hour = db.Column(db.Time)
    type_day = db.Column(db.String(20))
    total_leave_days = db.Column(db.Integer)
    extra_hours = db.Column(db.Integer)
    __table_args__ = (
        db.UniqueConstraint("person_id", "workday", name="unique_personid_workday"),
    )
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"))

    def __repr__(self):
        return f"{self.workday}; {self.type_day}"


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_hours_off_a_year = db.Column(db.Float, nullable=False)
    total_hours_in_one_full_workday = db.Column(db.Float, nullable=False)
    extra_minutes_left_from_last_year = db.Column(db.Integer)
    employees = db.relationship(
        "Employee", backref="worker", lazy=True
    )  # kept the wrongly chosen name from above
