import csv
import io
import json
import os.path

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    make_response
)

from application.models import LocalAuthority, ViabilityAssessment

viability = Blueprint('viability', __name__, template_folder='templates', url_prefix='/viability')


@viability.route('/')
def index():
    no_of_viability_assessments = len(ViabilityAssessment.query.all())
    local_authorities = [la for la in LocalAuthority.query.all() if la.has_viability_assessments()]
    return render_template('/viability-index.html',
                           no_of_viability_assessments=no_of_viability_assessments,
                           local_authorities=local_authorities)


@viability.route('/viability-assessments.json')
def index_json():
    no_of_viability_assessments = len(ViabilityAssessment.query.all())
    local_authorities = [la for la in LocalAuthority.query.all() if la.has_viability_assessments()]
    all = []
    for la in local_authorities:
        vas = []
        lav = {'local-authority-name': la.name, 'local-authority-id': la.id}
        for pa in la.planning_applications:
            for va in pa.viability_assessments:
                vas.append(va.to_dict())

        lav['viability-assessments'] = vas
        all.append(lav)

    return jsonify({'number-of-viablity-assessments': no_of_viability_assessments,
                    'local-authorities': len(local_authorities),
                    'viability-assessments': all})


@viability.route('/viability-assessments.csv')
def index_csv():

    input = io.StringIO()
    writer = csv.writer(input, quoting=csv.QUOTE_ALL,  delimiter=',')
    rows = [['local-authority-name',
             'local-authority-id',
             'planning-application-reference',
             'planning-application-url',
             'site',
             'viability-assessment-reference',
             'viability-assessment-url',
             'publication-date',
             'gross-development-value',
             'benchmark-land-value',
             'total-contributions']]

    local_authorities = [la for la in LocalAuthority.query.all() if la.has_viability_assessments()]
    for la in local_authorities:
        for pa in la.planning_applications:
            for va in pa.viability_assessments:
                rows.append([la.name,
                             la.id,
                             pa.reference,
                             pa.url,
                             pa.address,
                             va.id,
                             va.url,
                             va.date,
                             va.gross_development_value,
                             va.benchmark_land_value,
                             va.total_contribution])

    writer.writerows(rows)
    output = make_response(input.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=viability-assessments.csv"
    output.headers["Content-type"] = "text/csv"

    return output


@viability.route('/local-authority', methods=['GET', 'POST'])
def local_authority():

    if request.method == 'POST':
        return redirect(url_for('viability.local_authority_assessments', local_authority=request.form['local-authority-select']))

    return render_template('/viability-local-authority.html', localauthorities=LocalAuthority.query.all())


@viability.route('/local-authority/<local_authority>')
def local_authority_assessments(local_authority):
    la = LocalAuthority.query.get(local_authority)
    return render_template('/la-viability-assessments.html', localauthority=la)

@viability.route('/guidance')
def guidance():
    return render_template('/viability-guidance.html')

# =====================================================
# Routes for the (incomplete) viability summary journey
# =====================================================

@viability.route('/create-summary')
def start():
    return render_template('v-start-page.html')


@viability.route('/create-summary/select-local-authority', methods=['GET', 'POST'])
def create_summary():
    datafile = "application/data/localauthorities.json"
    if os.path.isfile(datafile):
        with open(datafile) as data_file:
            localauthorities = json.load(data_file)
    return render_template('v-local-authority.html', localauthorities=localauthorities['authorities'])


@viability.route('/create-summary/report-details')
def report_details():
    return render_template('v-report-details.html')


@viability.route('/create-summary/question')
def question():
    return render_template('v-question.html')


@viability.route('/create-summary/check-your-answers')
def check():
    return render_template('v-check-your-answers.html')


@viability.route('/create-summary/complete')
def complete():
    return render_template('v-complete.html')
