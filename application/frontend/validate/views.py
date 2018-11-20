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

            # Colm at the moment this just validates against schema for first type of file (developer-agreement.csv),
            # but it could be that the form that points here requires user to choose type
            # e.g. developer-agreement.csv, developer-agreement-contribution.csv or developer-agreement-transaction.csv
            # or there could be one page per type? Up to you.
            # Also the report page dumps the report straight into page, sorry :)
            # Try uploading tests/data/test-developer-agreement-invalid.csv and
            # tests/data/test-developer-agreement-valid.csv to see the report.

            report = goodtables.validate(developer_agreement_csv, schema=developer_agreement_schema)

            return render_template('validation-report.html', filename=filename, report=report)

    return render_template('validate.html', form=form)



