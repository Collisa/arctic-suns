from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from toestellen.models import ArcticSun
from toestellen.forms import Input
from flask_login import login_required


@app.route('/toestellen/<string:device_type>/all', methods=["GET"])
@login_required
def showAll(device_type):
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.type == device_type)
    return render_template("toestellen/view.html", template_form=Input(), all_arctic_suns=all_arctic_suns, device_type=device_type)


@app.route('/toestellen', methods=["GET"], defaults={'device_type': None})
@app.route('/toestellen/<string:device_type>', methods=["GET"])
@login_required
def arcticsun_index(device_type):
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None, ArcticSun.type == device_type)
    return render_template("toestellen/view.html", template_form=Input(), all_arctic_suns=all_arctic_suns, device_type=device_type)


@app.route('/add', methods=["POST"])
@login_required
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
            remarks=form.remarks.data,
            type=form.type.data)
        db.session.add(arctic_sun)
        db.session.commit()
    return redirect(url_for('arcticsun_index', device_type=form.type.data ))    



@app.route('/delete', methods=['POST'])
@login_required
def delete():
    item_to_delete = ArcticSun.query.filter_by(id=request.form['id']).first()
    db.session.delete(item_to_delete)
    db.session.commit()
    return ""


@app.route('/change/<int:id>', methods=['GET','POST'])
@login_required
def change(id):
    item_to_change = ArcticSun.query.get(id)
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None, ArcticSun.type == item_to_change.type)
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
        return redirect(url_for('arcticsun_index', device_type=item_to_change.type))
    return render_template("toestellen/view.html", template_form=Input(obj=item_to_change), all_arctic_suns=all_arctic_suns, edit=True, edit_id=item_to_change.id, device_type=item_to_change.type)