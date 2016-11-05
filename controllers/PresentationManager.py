__author__ = 'RiteshReddy'

from datetime import datetime, date
import os

from flask import render_template, request, send_from_directory

from flaskappbase import app
from models.BhajanModel import BhajanModel
from ppt.Presentation import SaiPresentation

@app.route("/presentationmanager", methods=["GET"])
def presentation_add_and_sort():
    bhajans = BhajanModel.get_all_bhajans()
    bhajans = sorted(bhajans, key=lambda x: x['name'])
    title = "Central London Sai Centre"
    subtitle = date.today().strftime("%B %d, %Y")
    return render_template('presentationmanager.html', bhajans=bhajans, title=title, subtitle=subtitle)

@app.route("/presentationmanager/generate", methods=["POST"])
def generate_presentation_experimental():
    form_dict = request.form.to_dict(flat=False)
    title = form_dict['title'][0] # form_dict contains an list, get the first element
    subtitle = form_dict['subtitle'][0] # form_dict contains an list, get the first element
    presentation = SaiPresentation(title, subtitle)
    if not 'bhajan_id' in form_dict:
        filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
        presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))
        return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)
    bhajan_ids = form_dict['bhajan_id']
    bhajan_text_adjusted = form_dict['bhajan']
    keys = form_dict['key']
    bhajans = BhajanModel.get_bhajans_if_they_exist(bhajan_ids)
    together = zip(bhajans, keys, bhajan_text_adjusted)

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
    presentation.add_bhajan_slide("", "", "") # filler slide at end.
    filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
    presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))

    return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)
