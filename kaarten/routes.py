from flask import render_template, request, redirect, url_for
from app import app, db
from kaarten.forms import CardForm
from kaarten.models import Card
from flask_login import login_required, current_user

kaarten = True


@app.route("/kaarten", methods=["GET"])
@login_required
def kaart_index():
    if current_user.firm == "Collibri":
        all_cards = Card.query.filter(Card.date_retour == None)
        return render_template(
            "kaarten/index.html",
            template_form=CardForm(),
            all_cards=all_cards,
            current_user=current_user,
            kaarten=kaarten,
        )


@app.route("/kaarten/all", methods=["GET"])
@login_required
def kaart_show_all():
    if current_user.firm == "Collibri":
        all_cards = Card.query.all()
        return render_template(
            "kaarten/index.html",
            template_form=CardForm(),
            all_cards=all_cards,
            current_user=current_user,
            kaarten=kaarten,
        )


@app.route("/kaart/add", methods=["POST"])
@login_required
def add_card():
    if current_user.firm == "Collibri":
        form = CardForm(request.form)

        if request.method == "POST":
            card = Card(
                card=form.card.data,
                date_retour=form.date_retour.data,
                date_out=form.date_out.data,
                chauffeur=form.chauffeur.data,
            )
            db.session.add(card)
            db.session.commit()
        return redirect(url_for("kaart_index"))


@app.route("/kaart/delete", methods=["POST"])
@login_required
def delete_card():
    if current_user.firm == "Collibri":
        item_to_delete = Card.query.filter_by(id=request.form["id"]).first()
        item_to_delete.delete()
        db.session.commit()
        return ""


@app.route("/kaart/change/<int:id>", methods=["GET", "POST"])
@login_required
def change_card(id):
    if current_user.firm == "Collibri":
        all_cards = Card.query.filter(Card.date_out == None)
        item_to_change = Card.query.get(id)
        form = CardForm(request.form)

        if request.method == "POST":
            item_to_change.card = form.card.data
            item_to_change.date_retour = form.date_retour.data
            item_to_change.date_out = form.date_out.data
            item_to_change.chauffeur = form.chauffeur.data
            db.session.commit()
            return redirect(url_for("kaart_index"))

        return render_template(
            "kaarten/index.html",
            template_form=CardForm(obj=item_to_change),
            all_cards=all_cards,
            edit=True,
            edit_id=item_to_change.id,
            current_user=current_user,
        )
