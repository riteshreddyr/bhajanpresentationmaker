__author__ = 'RiteshReddy'

from controllers.BhajanManager import *
from controllers.PresentationManager import *

def error_handler(e):
    return render_template("generic_error.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
