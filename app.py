from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
from flask_migrate import Migrate

app = Flask(__name__)



app.config['SECRET_KEY'] = 'c5723c7a0956175ca1e56086adc6bdc18064d2659be3b04fcd3bb89d1fbfe482'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///arctic_DB2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
 


class ArcticSun(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    date_in = db.Column(db.Date)
    date_out = db.Column(db.Date)
    pick_up_location = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    status = db.Column(db.String(15))
    remarks = db.Column(db.String(100))

    # def __init__(self, id, name, date_in, date_out, pick_up_location, destination, status):
    #     self.id = id
    #     self.name = name
    #     self.date_in = date_in
    #     self.date_out = date_out
    #     self.pick_up_location = pick_up_location
    #     self.destination = destination
    #     self.status = status    

#db.create_all()


class Input(FlaskForm):
    name = StringField("Arctic sun SN")
    date_in = DateField("Afhaling")
    date_out = DateField("Levering")
    pick_up_location = TextAreaField("Afhaallocatie")
    destination = TextAreaField("Leverlocatie")
    status = StringField("Status")
    submit = SubmitField("Toevoegen")
    remarks = TextAreaField("Opmerkingen")



@app.route('/all', methods=["GET"])
def showAll():
    all_arctic_suns = ArcticSun.query.all()
    return render_template("index.html", template_form=Input(), all_arctic_suns=all_arctic_suns)


@app.route('/', methods=["GET"])
def index():
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None)
    return render_template("index.html", template_form=Input(), all_arctic_suns=all_arctic_suns)


@app.route('/add', methods=["POST"])
def add():
    form = Input(request.form)
    if request.method == 'POST':
        arctic_sun = ArcticSun(
            name=form.name.data, 
            date_in=form.date_in.data,
            date_out=form.date_out.data,
            pick_up_location=form.pick_up_location.data, 
            destination=form.destination.data, 
            status=form.status.data,
            remarks=form.remarks.data)
        db.session.add(arctic_sun)
        db.session.commit()
    return redirect(url_for('index'))    



@app.route('/delete', methods=['POST'])
def delete():
    item_to_delete = ArcticSun.query.filter_by(id=request.form['id']).first()
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/change/<int:id>', methods=['GET','POST'])
def change(id):
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None)
    item_to_change = ArcticSun.query.get(id)
    print(item_to_change)
    form = Input(request.form)
    if request.method == 'POST':
        item_to_change.name=form.name.data
        item_to_change.date_in=form.date_in.data
        item_to_change.date_out=form.date_out.data
        item_to_change.pick_up_location=form.pick_up_location.data
        item_to_change.destination=form.destination.data
        item_to_change.status=form.status.data
        item_to_change.remarks=form.remarks.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("index.html", template_form=Input(obj=item_to_change), all_arctic_suns=all_arctic_suns, edit=True, edit_id=item_to_change.id)