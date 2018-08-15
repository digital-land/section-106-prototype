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

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
  return render_template('index.html')

@frontend.route('/start')
def start():
  session['section106'] = {}
  return render_template('start-page.html')


@frontend.route('/local-authority', methods=['GET', 'POST'])
def local_authority():
  if 'section106' in session:
    section106 = session['section106']
  if request.method == 'POST':
    section106['la_name'] = request.form['local-authority-selector']
    session['section106'] = section106
    return redirect(url_for('frontend.s106_ref'))
  datafile = "application/data/localauthorities.json"
  if os.path.isfile( datafile ):
    with open( datafile ) as data_file:
      localauthorities = json.load(data_file) 
  return render_template('local-authority.html', localauthorities=localauthorities['authorities'])

@frontend.route('/section-106-reference', methods=['GET', 'POST'])
def s106_ref():
  if 'section106' in session:
    section106 = session['section106']
  if request.method == 'POST':
    section106['agreement_reference'] = request.form['agreement-reference']
    session['section106'] = section106
    return redirect(url_for('frontend.pla_ref'))
  return render_template('section106-details.html')

@frontend.route('/planning-application-reference', methods=['GET', 'POST'])
def pla_ref():
  if 'section106' in session:
    section106 = session['section106']
  if request.method == 'POST':
    pla_ref = {
      'reference': request.form['planning-application-reference'],
      'url': request.form['planning-application-url']
    }
    section106['planning_application_reference'] = pla_ref
    session['section106'] = section106
    return redirect(url_for('frontend.developer_contributions'))
  return render_template('planning-application-details.html')

@frontend.route('/developer_contributions', methods=['GET', 'POST'])
def developer_contributions():
  if 'section106' in session:
    section106 = session['section106']
  if request.method == 'POST':
    return redirect(url_for('frontend.summary'))

  datafile = "application/data/parameters.json"
  if os.path.isfile( datafile ):
    with open( datafile ) as data_file:
      parameters = json.load(data_file) 
  return render_template('developer-contributions.html', parameters=parameters)

@frontend.route('/summary')
def summary():
  section106 = session['section106']
  return render_template('summary.html', s106=section106)

@frontend.context_processor
def asset_path_context_processor():
  return {'assetPath': '/static/govuk-frontend/assets'}