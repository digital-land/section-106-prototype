from flask import (
  Blueprint,
  render_template,
  redirect,
  request,
  session,
  url_for
)

import requests
import json
import os.path

viability = Blueprint('viability', __name__, template_folder='templates', url_prefix='/viability')


@viability.route('/')
def index():
  return render_template('index.html')