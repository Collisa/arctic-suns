



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