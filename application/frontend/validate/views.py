import os
import tempfile
import goodtables
import requests

from flask import Blueprint, render_template, current_app
from werkzeug.utils import secure_filename

from application.frontend.validate.forms import UploadForm

validators = Blueprint('validators', __name__, template_folder='templates')


@validators.route('/validate-start')
def validate_start():
    return render_template('validate-start.html')


@validators.route('/validate', methods=['GET', 'POST'])
def validate():

    form = UploadForm()

    if form.validate_on_submit():
        reports = []
        valid = True
        for file in form.upload.data:
            filename = secure_filename(file.filename)
            with tempfile.TemporaryDirectory() as temp_dir:
                csv_file = os.path.join(temp_dir, filename)
                validation_type = filename.split('.csv')[0]
                file.save(csv_file)
                schema_url = f"{current_app.config['BASE_SCHEMA_URL']}/{validation_type}-schema.json"
                resp = requests.get(schema_url)
                schema = resp.json()
                report = goodtables.validate(csv_file, schema=schema)
                valid = report['valid']
                reports.append({'file': filename, 'report': report})

        return render_template('validation-report.html', reports=reports, valid=valid)

    return render_template('validate.html', form=form)


