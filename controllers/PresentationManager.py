__author__ = 'RiteshReddy'

from datetime import datetime, date
import os
import json

from flask import render_template, request, send_from_directory
from flask import abort

from flaskappbase import app
from models.BhajanModel import BhajanModel
from ppt.Presentation import SaiPresentation
from werkzeug.utils import secure_filename

@app.route("/presentationmanager", methods=["GET"])
def presentation_add_and_sort():
    bhajans = BhajanModel.get_all_bhajans()
    bhajans = sorted(bhajans, key=lambda x: x['name'])
    title = "Central London Sai Centre"
    subtitle = date.today().strftime("%B %d, %Y")
    return render_template('presentationmanager.html', bhajans=bhajans, title=title, subtitle=subtitle)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/presentationmanager/saveState", methods=["POST"])
def save_state():
    form_dict = request.form.to_dict(flat=False)
    slide_title = form_dict['slideTitle'][0] # form_dict contains an list, get the first element
    subtitle = form_dict['slideSubtitle'][0] # form_dict contains an list, get the first element
    if not 'bhajan_id' in form_dict:
        # no bhajans were selected, going beyond is troublesome so just exit here.
        return abort(400)
    bhajan_id = form_dict['bhajan_id']
    title = form_dict['title']
    bhajan_text_adjusted = form_dict['bhajan']
    genders = form_dict['gender']
    keys = form_dict['key']
    together = zip(bhajan_id, title, genders, keys, bhajan_text_adjusted)

    bhajans_dict_list = list()
    for bhajan in together: # [bhajan_id, title, gender, key, bhajan_text_adjusted]
        bhajan_dict = {
            "id": bhajan[0],
            "title": bhajan[1],
            "gender": bhajan[2],
            "key": bhajan[3],
            "bhajan_text_adjusted": bhajan[4],
        }
        bhajans_dict_list.append(bhajan_dict)

    final_dict = {
        "title" : slide_title,
        "subtitle" : subtitle,
        "bhajans" : bhajans_dict_list
    }
    saved_state_json_filename = os.path.join(app.config['POWERPOINT_OUTPUT'], "savedState.json")
    with open(saved_state_json_filename, 'w') as saved_state_json_file:
        json.dump(final_dict, saved_state_json_file)

    filename = 'SaiBhajans_State_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.json'
    return send_from_directory(app.config['POWERPOINT_OUTPUT'], "savedState.json", as_attachment=True,
                               attachment_filename=filename)


@app.route("/presentationmanager/generate", methods=["POST"])
def generate_presentation():
    form_dict = request.form.to_dict(flat=False)
    slide_title = form_dict['slideTitle'][0] # form_dict contains an list, get the first element
    subtitle = form_dict['slideSubtitle'][0] # form_dict contains an list, get the first element
    presentation = SaiPresentation(slide_title, subtitle)
    if not 'bhajan_id' in form_dict:
        # no bhajans were selected, going beyond is troublesome so just exit here.
        filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
        presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))
        return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)
    title = form_dict['title']
    bhajan_text_adjusted = form_dict['bhajan']
    genders = form_dict['gender']
    keys = form_dict['key']
    together = zip(title, genders, keys, bhajan_text_adjusted)
    backgroundImageFile = request.files.get('backgroundImage')
    backgroundImage = None
    if backgroundImageFile and allowed_file(backgroundImageFile.filename):
        backgroundImage = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(backgroundImageFile.filename))
        backgroundImageFile.save(backgroundImage)
    hexTextColor = form_dict['textColor']
    if hexTextColor:
        hexTextColor = hexTextColor[0]

    for index in range(len(together) - 1):
        current = together[index]  # [title, gender, key, bhajan_text_adjusted]
        next = together[index + 1]  # [title, gender, key, bhajan_text_adjusted]
        bhajan_name = current[0]
        bhajan_txt = current[3]
        bhajan_key = current[2]
        bhajan_gender = current[1]
        next_bhajan_name = next[0]
        next_bhajan_gender = next[1]
        next_bhajan_key = next[2]
        presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_gender, bhajan_key, next_bhajan_name, next_bhajan_gender, next_bhajan_key, backgroundImage=backgroundImage, noBackground=form_dict.get('noBackground'), hexTextColor=hexTextColor)

    last = together[-1]  # [title, gender, key, bhajan_text_adjusted]
    bhajan_name = last[0]
    bhajan_txt = last[3] #last[0]['bhajan']
    bhajan_gender = last[1]
    bhajan_key = last[2]
    presentation.add_bhajan_slide(bhajan_name, bhajan_txt, bhajan_gender, bhajan_key, backgroundImage=backgroundImage, noBackground=form_dict.get('noBackground'), hexTextColor=hexTextColor)
    presentation.add_bhajan_slide("", "", "") # filler slide at end.
    filename = 'SaiBhajans_' + datetime.today().strftime("%d_%m_%Y_%H_%M_%S") + '.pptx'
    presentation.save_presentation(os.path.join(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx"))
    if backgroundImage:
        os.remove(backgroundImage)
    return send_from_directory(app.config['POWERPOINT_OUTPUT'], "bhajans.pptx", as_attachment=True,
                               attachment_filename=filename)
