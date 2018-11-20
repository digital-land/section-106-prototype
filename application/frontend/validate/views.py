import os
import tempfile
import goodtables

from flask import Blueprint, render_template, current_app
from werkzeug.utils import secure_filename

from application.frontend.validate.forms import UploadForm

validators = Blueprint('validators', __name__, template_folder='templates')


@validators.route('/validate', methods=['GET', 'POST'])
def validate():

    form = UploadForm()

    if form.validate_on_submit():
        file = form.upload.data
        filename = secure_filename(file.filename)
        with tempfile.TemporaryDirectory() as temp_dir:
            developer_agreement_csv = os.path.join(temp_dir, filename)
            file.save(developer_agreement_csv)
            data_directory = os.path.join(current_app.config['PROJECT_ROOT'], 'application', 'data')
            developer_agreement_schema = os.path.join(data_directory, 'developer-agreement-schema.json')
            report = goodtables.validate(developer_agreement_csv, schema=developer_agreement_schema)
            return render_template('validation-report.html', filename=filename, report=report)

    return render_template('validate.html', form=form)



