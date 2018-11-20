from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField


class UploadForm(FlaskForm):

    upload = FileField('file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'Only csv or files allowed')
    ])

    validation_type = SelectField(u'Type of section 106 data file you want to validate',
                                  choices=[('developer-agreement', 'Developer agreement'),
                                           ('developer-agreement-contribution', 'Developer agreement contribution'),
                                           ('developer-agreement-transation', 'Developer agreement transaction')])