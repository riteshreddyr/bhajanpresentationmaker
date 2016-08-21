__author__ = 'RiteshReddy'

from controllers.BhajanManager import *
from controllers.PresentationManager import *

def error_handler(e):
    return render_template("generic_error.html")

app.run(debug=True)
