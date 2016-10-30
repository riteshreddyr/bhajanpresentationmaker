__author__ = 'RiteshReddy'

from datetime import datetime
import os

from flask import render_template, request, send_from_directory

from flaskappbase import app
from models.BhajanModel import BhajanModel
from ppt.Presentation import SaiPresentation

@app.route("/presentationmanager", methods=["GET"])
def presentation_add_and_sort():
    bhajans = BhajanModel.get_all_bhajans()
    bhajans = sorted(bhajans, key=lambda x: x['name'])
    return render_template('presentationmanager.html', bhajans=bhajans)

@app.route("/presentationmanager/generate", methods=["POST"])
def generate_presentation_experimental():
    form_dict = request.form.to_dict(flat=False)
    bhajan_ids = form_dict['bhajan_id']
    bhajan_text_adjusted = form_dict['bhajan']
    keys = form_dict['key']
    bhajans = BhajanModel.get_bhajans_if_they_exist(bhajan_ids)
    together = zip(bhajans, keys, bhajan_text_adjusted)
    presentation = SaiPresentation()
    for index in range(len(together) - 1):
        current = together[index]  # [bhajan, key, bhajan_text_adjusted]
        next = together[index + 1]  # [bhajan, key, bhajan_text_adjusted]
        bhajan_name = current[0]['name']
        bhajan_txt = current[2] #current[0]['bhajan']
        bhajan_key = current[1]
        next_bhajan_name = next[0]['name']
        next_bhajan_key = next[1]
        presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_key, next_bhajan_name, next_bhajan_key)

    last = together[-1]  # [bhajan, key, bhajan_text_adjusted]
    bhajan_name = last[0]['name']
    bhajan_txt = last[2] #last[0]['bhajan']
    bhajan_key = last[1]
    presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_key)
    filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
    presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))

    return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)
