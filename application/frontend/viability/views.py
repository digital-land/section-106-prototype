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
def start():
  return render_template('v-start-page.html')

@viability.route('/local-authority', methods=['GET', 'POST'])
def local_authority():
  datafile = "application/data/localauthorities.json"
  if os.path.isfile( datafile ):
    with open( datafile ) as data_file:
      localauthorities = json.load(data_file) 
  return render_template('v-local-authority.html', localauthorities=localauthorities['authorities'])

@viability.route('/question')
def question():
  return render_template('v-question.html')