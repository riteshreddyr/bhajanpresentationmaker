__author__ = 'RiteshReddy'

import os

from flask import render_template, request, redirect, send_from_directory, flash, jsonify

from flaskappbase import app
from models.BhajanModel import BhajanModel


@app.route("/bhajanmanager", methods=["GET"])
def list_all_bhajans():
    bhajans = BhajanModel.get_all_bhajans()
    bhajans = sorted(bhajans, key=lambda x: x['name'])
    return render_template('bhajanmanager_index.html', bhajans=bhajans)


@app.route("/bhajanmanager/add", methods=["GET", "POST"])
def add_bhajan():
    if request.method == "POST":
        name, bhajan, meaning = _get_bhajan_from_request(request)
        if name is None or bhajan is None:
            return render_template("generic_error.html")
        if not name is None and (bhajan is None or len(bhajan) == 0):
            return render_template("bhajanmanager_add.html", error="Please fill in the bhajan text")
        if not bhajan is None and (name is None or len(name) == 0):
            return render_template("bhajanmanager_add.html", error="Please fill in the bhajan name")
        id = BhajanModel.add_bhajan(name, bhajan, meaning)
        return redirect('/bhajanmanager/edit/' + str(id) + "?just_added=true")
    else:
        return render_template('bhajanmanager_add.html')


@app.route("/bhajanmanager/edit/<bhajan_id>", methods=["GET", "POST"])
def edit_bhajan(bhajan_id):
    if request.args.get('just_added', 'false') == 'true':
        just_added = True
    else:
        just_added = False
    if request.method == "POST":
        name, bhajan, meaning = _get_bhajan_from_request(request)
        if name is None or bhajan is None:
            return render_template("generic_error.html")
        if not name is None and (bhajan is None or len(bhajan) == 0):
            return render_template("bhajanmanager_edit.html", id=bhajan_id, name=name, bhajan=bhajan, meaning=meaning,
                                   error="Please fill in the bhajan text")
        if not bhajan is None and (name is None or len(name) == 0):
            return render_template("bhajanmanager_edit.html", id=bhajan_id, name=name, bhajan=bhajan, meaning=meaning,
                                   error="Please fill in the bhajan name")
        BhajanModel.edit_bhajan(bhajan_id, name, bhajan, meaning)
    bhajan = BhajanModel.get_bhajan(bhajan_id)
    return render_template('bhajanmanager_edit.html', id=bhajan_id, name=bhajan['name'], bhajan=bhajan['bhajan'],
                           meaning=bhajan['meaning'], just_added=just_added)


@app.route("/bhajanmanager/delete/<bhajan_id>", methods=["GET"])
def delete_bhajan(bhajan_id):
    BhajanModel.delete_bhajan(bhajan_id)
    return redirect("/bhajanmanager")


@app.route("/bhajanmanager/export", methods=["GET"])
def export_bhajans():
    return send_from_directory(app.config['DATA_DIRECTORY'], "bhajans.json", as_attachment=True, attachment_filename="bhajans.json")


@app.route("/bhajanmanager/import", methods=["GET", "POST"])
def import_bhajans():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No selected file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = file.filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)

        success = BhajanModel.import_bhajans(filename)
        if not success:
            flash("Something went wrong, is the file format correct?")
            return redirect(request.url)

        flash("Successfully Imported")
        return redirect(request.url)
    else:
        return render_template('bhajanmanager_import.html', error=False)


def _get_bhajan_from_request(request):
    if not request.form is None:
        return request.form['name'], request.form['bhajan'], request.form['meaning']
    stream = request.stream.read()
    if not stream is None or len(stream) != 0:
        # sometimes we get it as a parameter string here.
        split = stream.split('&')
        name = split[0].split('=')[1]
        bhajan = split[1].split('=')[1]
        meaning = split[2].split('=')[1]
        return name, bhajan, meaning
    return None, None, None

@app.route("/bhajanmanager/bhajanjson/<bhajan_id>", methods=["GET"])
def get_bhajan_json(bhajan_id):
    if (bhajan_id == "-1"):
        return jsonify(BhajanModel.FILLER_SLIDE)
    bhajan = BhajanModel.get_bhajan(int(bhajan_id))
    if bhajan is None:
        return jsonify(dict())
    else:
        return jsonify(bhajan)