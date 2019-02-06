import csv
import os
import tempfile
import uuid
import boto3
import botocore
import goodtables
import requests

from datapackage import Package, Resource
from datapackage.exceptions import CastError, RelationError

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
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in form.upload.data:
                output_dir = f'{temp_dir}/data'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                filename = secure_filename(file.filename)
                csv_file = os.path.join(output_dir, filename)
                validation_type = filename.split('.csv')[0]
                file.save(csv_file)
                schema_url = f"{current_app.config['BASE_SCHEMA_URL']}/{validation_type}-schema.json"
                resp = requests.get(schema_url)
                schema = resp.json()
                report = goodtables.validate(csv_file, schema=schema)
                valid = report['valid']
                reports.append({'file': filename, 'report': report})
                if file.filename == 'developer-agreement.csv':
                    local_authority = _get_local_authority(csv_file)
            if valid and local_authority is not None:
                print('create data package for', local_authority)
                datapackage_url = _make_package(temp_dir, local_authority, current_app.config)
            else:
                datapackage_url = None

        return render_template('validation-report.html', reports=reports, valid=valid, datapackage_url=datapackage_url)

    return render_template('validate.html',
                           form=form)


def _make_package(source, publisher, config):

    os.chdir(source)
    files = [f for f in os.listdir('data') if f.endswith('.csv')]
    package = Package({'publisher': publisher})

    for f in files:
        path = f"data/{f}"
        name = f.replace('.csv', '')
        schema = f"https://raw.githubusercontent.com/digital-land/alpha-data/master/schema/{name}-schema.json"
        resource = Resource({'path': path, 'schema': schema})
        package.add_resource(resource.descriptor)

    package.commit()
    package.infer()

    errors = False
    for r in package.resources:
        try:
            r.read(keyed=True)
            r.check_relations()
        except (CastError, RelationError) as e:
            print('Error in', os.path.join(source, r.descriptor['path']))
            print(e, e.errors)
            errors = True
    if not errors:
        package.save('datapackage.zip')
        print('saved datapackage.json to', source)

        s3 = boto3.client(
            's3',
            aws_access_key_id = config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY']
        )

        bucket = 'developer-contributions-datapackages'
        key = f'{publisher}/{uuid.uuid4()}/datapackage.zip'
        s3.upload_file(f'{source}/datapackage.zip', bucket, key, ExtraArgs={'ACL': 'public-read'})

        config = s3._client_config
        config.signature_version = botocore.UNSIGNED

        datapackage_url = boto3.resource('s3', config=config).meta.client.generate_presigned_url('get_object',
                                                                                                  ExpiresIn=0,
                                                                                                  Params={'Bucket': bucket,
                                                                                                         'Key': key})

        return datapackage_url


def _get_local_authority(csv_file):
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            local_authority = row.get('organisation', None)
            if local_authority is not None:
                break
        return local_authority
