from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from wtforms.validators import DataRequired, ValidationError


class UploadForm(FlaskForm):

    upload = MultipleFileField('Files', validators=[DataRequired()])

    @staticmethod
    def validate_upload(field, data):
        files = field.data[data.name]
        if len(files) > 3:
            raise ValidationError('Upload a maximum of 3 files')
        