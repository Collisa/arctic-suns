from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from models import ArcticSun
from forms import RegistrationForm, LoginForm, Input
from models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/all', methods=["GET"])
@login_required
def showAll():
    all_arctic_suns = ArcticSun.query.all()
    return render_template("arcticsun/index.html", template_form=Input(), all_arctic_suns=all_arctic_suns)


@app.route('/index', methods=["GET"])
@login_required
def arcticsun_index():
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None)
    return render_template("arcticsun/index.html", template_form=Input(), all_arctic_suns=all_arctic_suns)


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
            remarks=form.remarks.data)
        db.session.add(arctic_sun)
        db.session.commit()
    return redirect(url_for('arcticsun_index'))    



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
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.date_out == None)
    item_to_change = ArcticSun.query.get(id)
    if request.method == 'POST':
        form = Input(request.form)
        item_to_change.name=form.name.data
        item_to_change.date_in=form.date_in.data
        item_to_change.date_out=form.date_out.data
        item_to_change.pick_up_location=form.pick_up_location.data
        item_to_change.destination=form.destination.data
        item_to_change.status=form.status.data
        item_to_change.remarks=form.remarks.data
        db.session.commit()
        return redirect(url_for('arcticsun_index'))
    return render_template("arcticsun/index.html", template_form=Input(obj=item_to_change), all_arctic_suns=all_arctic_suns, edit=True, edit_id=item_to_change.id)


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "succes")
        return redirect(url_for("arcticsun_index"))
    return render_template("authentication/register.html", title="Register", form=form)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("arcticsun_index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('arcticsun_index'))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("authentication/login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))