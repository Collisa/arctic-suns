from flask import render_template, request, redirect, url_for
from app import app, db
from toestellen.models import ArcticSun
from toestellen.forms import Input
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import and_, or_


def redirect_url(default="arcticsun_index"):
    return request.args.get("next") or request.referrer or url_for(default)


@app.route("/toestellen/<string:device_type>/all", methods=["GET"])
@login_required
def showAll(device_type):
    alle = True
    now = datetime.now().date()
    all_arctic_suns = ArcticSun.query.filter(ArcticSun.type == device_type)
    return render_template(
        "toestellen/view.html",
        template_form=Input(),
        all_arctic_suns=all_arctic_suns,
        device_type=device_type,
        current_user=current_user,
        alle=alle,
        now=now,
    )


@app.route("/toestellen", methods=["GET"], defaults={"device_type": None})
@app.route("/toestellen/<string:device_type>", methods=["GET"])
@login_required
def arcticsun_index(device_type):
    alle = False
    now = datetime.now().date()

    all_arctic_suns = ArcticSun.query.filter(
        and_(
            or_(
                ArcticSun.date_out >= datetime.now() - timedelta(days=1),
                ArcticSun.date_out == None,
            ),
            ArcticSun.type == device_type,
            ArcticSun.destination != None,
        )
    )
    return render_template(
        "toestellen/view.html",
        template_form=Input(),
        all_arctic_suns=all_arctic_suns,
        device_type=device_type,
        current_user=current_user,
        alle=alle,
        now=now,
    )


@app.route("/toestellen/<string:device_type>/CRS", methods=["GET"])
@login_required
def arcticsun_at_crs(device_type):
    alle = False
    CRS = True
    now = datetime.now().date()

    all_arctic_suns = ArcticSun.query.filter(
        and_(
            or_(
                ArcticSun.destination.contains("CRS"),
                ArcticSun.destination.contains("Asslar"),
                ArcticSun.destination.contains("Aßlar"),
                ArcticSun.destination.contains("asslar"),
                ArcticSun.destination.contains("crs"),
            ),
            ArcticSun.type == "arctic",
            or_(ArcticSun.returned_from_crs == None, ArcticSun.returned_from_crs == 0),
        )
    )
    return render_template(
        "toestellen/view.html",
        template_form=Input(),
        all_arctic_suns=all_arctic_suns,
        device_type=device_type,
        current_user=current_user,
        alle=alle,
        now=now,
        CRS=CRS,
    )


@app.route("/toestellen/<string:device_type>/CRS/<int:id>", methods=["POST"])
@login_required
def change_crs_state(device_type, id):
    if current_user.firm == "Collibri":
        item_to_change = ArcticSun.query.get(id)
        item_to_change.returned_from_crs = True
        db.session.commit()
        return redirect(url_for("arcticsun_at_crs", device_type=device_type))


@app.route("/add", methods=["POST"])
@login_required
def add():
    if current_user.firm == "Collibri":
        form = Input(request.form)

        if request.method == "POST":
            arctic_sun = ArcticSun(
                name=form.name.data,
                date_in=form.date_in.data,
                date_out=form.date_out.data,
                pick_up_location=form.pick_up_location.data,
                destination=form.destination.data,
                status=form.status.data,
                remarks=form.remarks.data,
                type=form.type.data,
            )
            db.session.add(arctic_sun)
            db.session.commit()
        return redirect(redirect_url())


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    if current_user.firm == "Collibri":
        item_to_delete = ArcticSun.query.filter_by(id=request.form["id"]).first()
        item_to_delete.delete()
        db.session.commit()
        return ""


@app.route("/change/<int:id>", methods=["GET"])
@login_required
def change(id):
    if current_user.firm == "Collibri":
        item_to_change = ArcticSun.query.get(id)
        all_arctic_suns = ArcticSun.query.filter(
            ArcticSun.date_out == None, ArcticSun.type == item_to_change.type
        )

        return render_template(
            "toestellen/edit.html",
            template_form=Input(obj=item_to_change),
            all_arctic_suns=all_arctic_suns,
            edit_id=item_to_change.id,
            device_type=item_to_change.type,
            item_to_change=item_to_change,
        )


@app.route("/change/<int:id>/change", methods=["POST"])
@login_required
def change_change(id):
    if current_user.firm == "Collibri":
        item_to_change = ArcticSun.query.get(id)

        form = Input(request.form)

        item_to_change.name = form.name.data
        item_to_change.date_in = form.date_in.data
        item_to_change.date_out = form.date_out.data
        item_to_change.pick_up_location = form.pick_up_location.data
        item_to_change.destination = form.destination.data
        item_to_change.status = form.status.data
        item_to_change.remarks = form.remarks.data
        db.session.commit()
        return redirect(url_for("arcticsun_index", device_type=item_to_change.type))
