__author__ = 'RiteshReddy'
import os
from flask import Flask, render_template
app = Flask(__name__)

app.secret_key = "NoSecretsFromSai"
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "uploads")
app.config['POWERPOINT_OUTPUT'] = os.path.join(app.root_path, "generated_ppts")
app.config['DATA_DIRECTORY'] = os.path.join(app.root_path, 'data')
app.config['BHAJAN_SOURCE_FILE'] = os.path.join(app.config['DATA_DIRECTORY'], 'bhajans.json')


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['POWERPOINT_OUTPUT']):
    os.makedirs(app.config['POWERPOINT_OUTPUT'])

if not os.path.exists(app.config['DATA_DIRECTORY']):
    os.makedirs(app.config['DATA_DIRECTORY'])

@app.route("/")
def hello():
    return render_template("index.html")

