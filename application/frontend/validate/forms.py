from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import MultipleFileField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):

    upload = MultipleFileField('Files', validators=[DataRequired()])