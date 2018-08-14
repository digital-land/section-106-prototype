import requests
from flask import (
  Blueprint,
  render_template,
  request
)

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
  return render_template('index.html')


@frontend.context_processor
def asset_path_context_processor():
  return {'assetPath': '/static/govuk-frontend/assets'}