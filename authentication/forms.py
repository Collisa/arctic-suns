from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from authentication.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Paswoord", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Bevestig Paswoord", validators=[DataRequired(), EqualTo("password")]
    )
    firm = SelectField(
        "Firma",
        choices=[("BARD/BD", "BARD/BD"), ("Collibri", "Collibri")],
        validators=[DataRequired()],
    )
    function = SelectField(
        "Functie",
        choices=[("BARD", "BARD"), ("werknemer", "werknemer"), ("admin", "admin")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Registreer")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Paswoord", validators=[DataRequired()])
    remember = BooleanField("Onthoud Me")
    submit = SubmitField("Log In")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Paswoord")

    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Er bestaat nog geen account voor dit emailadres.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Paswoord", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Bevestig Paswoord", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Paswoord")
