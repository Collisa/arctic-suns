from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db, bcrypt, mail
from authentication.models import User
from authentication.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from os import environ



@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if current_user.firm == "Collibri":
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_pw, firm=form.firm.data, function=form.function.data)
            db.session.add(user)
            db.session.commit()
            flash("The account has been created! You are now able to log in.", "succes")
            return redirect(url_for("arcticsun_index", device_type="arctic"))
        return render_template("authentication/register.html", title="Register", form=form)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("arcticsun_index", device_type="arctic"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('arcticsun_index', device_type="arctic"))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("authentication/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Paswoord reset', sender=environ.get('MAIL_SENDER'), recipients=[user.email])
    msg.body = f"""Om je paswoord te resetten, klik op onderstaande link:
{url_for('reset_token', token=token, _external=True)}
Als je geen aanvraag hebt gedaan om je paswoord te wijzigen kan je deze mail gewoon negeren."""
    mail.send(msg)


@app.route("/reset_paswoord", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("arcticsun_index", device_type="arctic"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Er is een email verstuurd met instructies om uw paswoord te resetten.', 'succes')
        return redirect(url_for('login'))
    return render_template("authentication/reset_request.html", form=form)


@app.route("/reset_paswoord/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("arcticsun_index", device_type="arctic"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('De token voor de reset is ongeldig of verlopen', 'info')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pw
        db.session.commit()
        flash("Uw paswoord is gereset. Je kan nu terug inloggen.", "succes")
        return redirect(url_for("login"))
    return render_template("authentication/reset_token.html", form=form)
