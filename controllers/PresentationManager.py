__author__ = 'RiteshReddy'

from datetime import datetime
import os

from flask import render_template, request, send_from_directory

from flaskappbase import app
from models.BhajanModel import BhajanModel
from ppt.Presentation import SaiPresentation


@app.route("/presentationmanager", methods=["GET"])
def presentation_start():
    bhajans = BhajanModel.get_all_bhajans()
    bhajans = sorted(bhajans, key=lambda x: x['name'])
    return render_template("presentationmanager_start.html", bhajans=bhajans)


@app.route("/presentationmanager/sort", methods=["POST"])
def presentation_sort_and_add_key():
    bhajans_chosen = request.form.getlist('bhajans_chosen')
    filler_slides = request.form['fillerSlides']
    bhajans_chosen = BhajanModel.get_bhajans_if_they_exist(bhajans_chosen)
    return render_template('presentationmanager_sort.html', bhajans_chosen=bhajans_chosen,
                           filler_slides=int(filler_slides))


@app.route("/presentationmanager/generate", methods=["POST"])
def generate_presentation():
    form_dict = request.form.to_dict(flat=False)
    bhajan_ids = form_dict['bhajan_id']
    positions = form_dict['position']
    keys = form_dict['key']
    bhajans = BhajanModel.get_bhajans_if_they_exist(bhajan_ids)
    together = zip(positions, bhajans, keys)
    together = sorted(together, key=lambda x: int(x[0]))
    presentation = SaiPresentation()
    for index in range(len(together) - 1):
        current = together[index]  # [position, bhajan, key]
        next = together[index + 1]  # [position, bhajan, key]
        bhajan_name = current[1]['name']
        bhajan_txt = current[1]['bhajan']
        bhajan_key = current[2]
        next_bhajan_name = next[1]['name']
        next_bhajan_key = next[2]
        presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_key, next_bhajan_name, next_bhajan_key)

    last = together[-1]  # [position, bhajan, key]
    bhajan_name = last[1]['name']
    bhajan_txt = last[1]['bhajan']
    bhajan_key = last[2]
    presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_key)
    filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
    presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))

    return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)