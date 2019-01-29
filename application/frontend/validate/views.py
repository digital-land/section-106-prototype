import os
import tempfile
import goodtables
import requests

from flask import Blueprint, render_template, current_app, url_for
from werkzeug.utils import secure_filename, redirect

from application.frontend.validate.forms import UploadForm, ValidationSelectionForm

validators = Blueprint('validators', __name__, template_folder='templates')


@validators.route('/validate-start')
def validate_start():
    return render_template('validate-start.html')


@validators.route('/validate', methods=['GET', 'POST'])
def validation_selection():

    form = ValidationSelectionForm()

    if form.validate_on_submit():
        return redirect(url_for('validators.validate_by_type', validation_type=form.validation_type.data))

    return render_template('validation-selection.html', form=form)


@validators.route('/validate/<validation_type>', methods=['GET', 'POST'])
def validate_by_type(validation_type):

    form = UploadForm()

    if form.validate_on_submit():
        file = form.upload.data
        filename = secure_filename(file.filename)
        with tempfile.TemporaryDirectory() as temp_dir:
            developer_agreement_csv = os.path.join(temp_dir, filename)
            file.save(developer_agreement_csv)
            schema_url = f"{current_app.config['BASE_SCHEMA_URL']}/{validation_type}-schema.json"
            resp = requests.get(schema_url)
            schema = resp.json()
            report = goodtables.validate(developer_agreement_csv, schema=schema)
            return render_template('validation-report.html', filename=filename, report=report)

    return render_template('validate.html', form=form, validation_type=validation_type)



