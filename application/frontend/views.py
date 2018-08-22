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
from application.models import LocalAuthority, PlanningApplication, Contribution

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def start():
    session['section106'] = {}
    return render_template('start-page.html')


@frontend.route('/local-authority', methods=['GET', 'POST'])
def local_authority():

    if request.method == 'POST':
        return redirect(url_for('frontend.pla_ref', local_authority=request.form['local-authority-selector']))
    return render_template('local-authority.html', localauthorities=LocalAuthority.query.all())

def getDateFromForm(form):
    return '{}-{}-{}'.format(form['section106-signed-day'], form['section106-signed-month'],
                             form['section106-signed-year'])


@frontend.route('/local-authority/<local_authority>/planning-application', methods=['GET', 'POST'])
def pla_ref(local_authority):

    if request.method == 'POST':

        planning_reference = request.form['planning-application-reference']
        url = request.form['planning-application-url']
        local_authority = LocalAuthority.query.get(local_authority)
        application = PlanningApplication(reference=planning_reference, url=url, local_authority=local_authority)

        db.session.add(application)
        db.session.commit()

        return redirect(url_for('frontend.s106_details',
                                local_authority=local_authority.id,
                                planning_reference=planning_reference))

    return render_template('planning-application-details.html',
                           local_authority=local_authority)


@frontend.route('/local-authority/<local_authority>/planning-application/<planning_reference>', methods=['GET', 'POST'])
def s106_details(local_authority, planning_reference):

    if request.method == 'POST':
        reference = request.form['agreement-reference']
        signed_date = getDateFromForm(request.form)
        planning_application = PlanningApplication.query.filter_by(local_authority_id=local_authority, reference=planning_reference).one()
        planning_application.section106_signed_date = signed_date
        planning_application.section106_url = reference
        db.session.add(planning_application)
        db.session.commit()

        return redirect(url_for('frontend.developer_contributions',
                                local_authority=local_authority,
                                planning_reference=planning_application.reference))

    return render_template('section106-details.html',
                           local_authority=local_authority,
                           planning_reference=planning_reference,
                           other_agreements=[])


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


@frontend.route('/local-authority/<local_authority>/planning-application/<planning_reference>/developer-contributions', methods=['GET', 'POST'])
def developer_contributions(local_authority, planning_reference):

    if request.method == 'POST':
        contributions = extractAllContributions(request.form)
        agreement = PlanningApplication.query.filter_by(reference=planning_reference,
                                                        local_authority_id=local_authority).one()
        for contribution in contributions:
            c = Contribution()
            c.contribution_type = contribution['type']
            c.category = contribution['category']
            c.obligation = contribution['obligation']
            c.value = contribution['value']
            agreement.section106_contributions.append(c)

        db.session.add(agreement)
        db.session.commit()

        return redirect(url_for('frontend.summary', local_authority=local_authority, planning_reference=planning_reference))

    datafile = "application/data/parameters.json"
    if os.path.isfile(datafile):
        with open(datafile) as data_file:
            parameters = json.load(data_file)

    return render_template('developer-contributions.html',
                           parameters=parameters,
                           local_authority=local_authority,
                           planning_reference=planning_reference)


@frontend.route('/local-authority/<local_authority>/planning-application/<planning_reference>/summary')
def summary(local_authority, planning_reference):

    planning_application = PlanningApplication.query.filter_by(reference=planning_reference,
                                                    local_authority_id=local_authority).one()

    return render_template('summary.html', application=planning_application)


@frontend.route('/complete')
def complete():
    return render_template('complete.html')


@frontend.context_processor
def asset_path_context_processor():
    return {'assetPath': '/static/govuk-frontend/assets'}
