from flask import (
  Blueprint,
  render_template,
  request
)

import requests
import json
import os.path

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
  return render_template('index.html')

@frontend.route('/start')
def start():
  return render_template('start-page.html')


@frontend.route('/local-authority')
def local_authority():
  datafile = "application/data/localauthorities.json"
  if os.path.isfile( datafile ):
    with open( datafile ) as data_file:
      localauthorities = json.load(data_file) 
  return render_template('local-authority.html', localauthorities=localauthorities['authorities'])

@frontend.context_processor
def asset_path_context_processor():
  return {'assetPath': '/static/govuk-frontend/assets'}