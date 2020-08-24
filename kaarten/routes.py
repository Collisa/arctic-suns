from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from kaarten.forms import CardForm
from kaarten.models import Card

@app.route('/kaarten', methods=["GET"])
def kaart_index():
    return render_template("kaarten/index.html", template_form=CardForm())