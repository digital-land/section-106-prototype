# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask.cli import load_dotenv


if os.environ['FLASK_ENV'] == 'production':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    register_errorhandlers(app)
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_filters(app)
    register_context_processors(app)
    return app


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("error/{0}.html".format(error_code)), error_code
    for errcode in [400, 401, 404, 500]:
        app.errorhandler(errcode)(render_error)
        return None


def register_blueprints(app):
    from application.frontend.views import frontend
    app.register_blueprint(frontend)

    from application.frontend.viability.views import viability
    app.register_blueprint(viability)


def register_extensions(app):

    from application.extensions import db
    db.init_app(app)

    from application.models import LocalAuthority
    from application.extensions import migrate
    migrate.init_app(app=app)


def register_commands(app):
    from application.commands import load, load_viability, clear_viability, load_contributions
    app.cli.add_command(load, name='load')
    app.cli.add_command(load_viability, name='load-viability')
    app.cli.add_command(clear_viability, name='clear-viability')
    app.cli.add_command(load_contributions, name='load-contribution')


def register_filters(app):
    from application.filters import readable_number_filter
    app.jinja_env.filters['readable_number'] = readable_number_filter

    from application.filters import monetary_filter
    app.jinja_env.filters['monetary'] = monetary_filter


def register_context_processors(app):

    @app.context_processor
    def _inject_asset_path():
        return {'assetPath': '/static'}

