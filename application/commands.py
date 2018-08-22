import csv
from contextlib import closing

import click
import requests
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def load():

    from application.extensions import db
    from application.models import LocalAuthority

    la_url = 'https://raw.githubusercontent.com/communitiesuk/digital-land-collector/master/data/organisation.tsv'
    print('Loading', la_url)
    with closing(requests.get(la_url, stream=True)) as r:
        reader = csv.DictReader(r.iter_lines(decode_unicode=True), delimiter='\t')
        for row in reader:
            if row['organisation'].startswith('local-authority'):
                la = LocalAuthority(id=row['organisation'],
                                    name=row['name'])
                db.session.add(la)
                db.session.commit()