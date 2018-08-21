from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    session,
    url_for
)

import json
import os.path

from application.extensions import db
from application.models import LocalAuthority, Section106Agreement, Contribution

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def start():
    session['section106'] = {}
    return render_template('start-page.html')


@frontend.route('/local-authority', methods=['GET', 'POST'])
def local_authority():

    if request.method == 'POST':
        return redirect(url_for('frontend.s106_ref', local_authority=request.form['local-authority-selector']))
    return render_template('local-authority.html', localauthorities=LocalAuthority.query.all())


def getDateFromForm(form):
    return '{}-{}-{}'.format(form['section106-signed-day'], form['section106-signed-month'],
                             form['section106-signed-year'])


@frontend.route('/local-authority/<local_authority>/section-106-reference', methods=['GET', 'POST'])
def s106_ref(local_authority):

    if request.method == 'POST':
        reference = request.form['agreement-reference']
        signed_date = getDateFromForm(request.form)
        local_authority = LocalAuthority.query.get(local_authority)
        section106_agreement = Section106Agreement(reference=reference, signed_date=signed_date, local_authority=local_authority)
        db.session.add(section106_agreement)
        db.session.commit()
        return redirect(url_for('frontend.pla_ref',
                                local_authority=local_authority.id,
                                section106_agreement=section106_agreement.reference))

    other_agreements = Section106Agreement.query.filter_by(local_authority_id=local_authority).all()

    return render_template('section106-details.html', local_authority=local_authority, other_agreements=other_agreements)


@frontend.route('/local-authority/<local_authority>/section-106-agreement/<section106_agreement>/planning-application-reference', methods=['GET', 'POST'])
def pla_ref(local_authority, section106_agreement):

    if request.method == 'POST':
        agreement = Section106Agreement.query.filter_by(reference=section106_agreement,
                                                        local_authority_id=local_authority).one()
        agreement.planning_application_reference = request.form['planning-application-reference']
        agreement.planning_application_url = request.form['planning-application-url']

        db.session.add(agreement)
        db.session.commit()

        return redirect(url_for('frontend.developer_contributions',
                                local_authority=local_authority,
                                section106_agreement=section106_agreement))

    return render_template('planning-application-details.html',
                           local_authority=local_authority,
                           section106_agreement=section106_agreement)


def getContribution(form, n):
    contribution = {
        'type': form['contribution-type-selector--{}'.format(n)],
        'category': form['contribution-category-selector--{}'.format(n)],
        'obligation': form['obligation-textarea--{}'.format(n)],
        'value': form['contribution-amount-input--{}'.format(n)]
    }
    return contribution


def extractAllContributions(form):
    contributions = []
    ids = [key for key, value in form.items() if 'contribution-type' in key.lower()]
    numbers = [item.split('--')[1] for item in ids]
    for n in numbers:
        contributions.append(getContribution(form, n))
    return contributions


@frontend.route('/local-authority/<local_authority>/section-106-agreement/<section106_agreement>/developer-contributions', methods=['GET', 'POST'])
def developer_contributions(local_authority, section106_agreement):

    if request.method == 'POST':
        contributions = extractAllContributions(request.form)
        agreement = Section106Agreement.query.filter_by(reference=section106_agreement,
                                                        local_authority_id=local_authority).one()
        for contribution in contributions:
            c = Contribution()
            c.contribution_type = contribution['type']
            c.category = contribution['category']
            c.obligation = contribution['obligation']
            c.value = contribution['value']
            agreement.contributions.append(c)

        db.session.add(agreement)
        db.session.commit()

        return redirect(url_for('frontend.summary', local_authority=local_authority, section106_agreement=section106_agreement))

    datafile = "application/data/parameters.json"
    if os.path.isfile(datafile):
        with open(datafile) as data_file:
            parameters = json.load(data_file)

    return render_template('developer-contributions.html',
                           parameters=parameters,
                           local_authority=local_authority,
                           section106_agreement=section106_agreement)


@frontend.route('/local-authority/<local_authority>/section-106-agreement/<section106_agreement>/summary')
def summary(local_authority, section106_agreement):

    agreement = Section106Agreement.query.filter_by(reference=section106_agreement,
                                                    local_authority_id=local_authority).one()

    return render_template('summary.html', s106=agreement)


@frontend.route('/complete')
def complete():
    return render_template('complete.html')


@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
