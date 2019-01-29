from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from wtforms.validators import DataRequired, ValidationError


allowed_files = set(['developer-agreement.csv',
                     'developer-agreement-contribution.csv',
                     'developer-agreement-transaction.csv'])

class UploadForm(FlaskForm):

    upload = MultipleFileField('Files', validators=[DataRequired()])

    @staticmethod
    def validate_upload(field, data):
        files = field.data[data.name]
        if len(files) > 3:
            raise ValidationError('Upload a maximum of 3 files')
        files = set(files)
        if not files <= allowed_files:
            raise ValidationError(f"Only the following files can be uploaded {','.join(allowed_files)}")
