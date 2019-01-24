import os
from flask import Flask
from flask_restplus import Api
from flask_migrate import Migrate


def create_app(debug=False, testing=False):
    # Create Flask App
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.debug = debug
    app.testing = testing

    # Create Database
    from soundsphere.database.db import db
    with app.app_context():
        db.init_app(app)

    migrate = Migrate(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create Routes
    from .api.albums import api as album_api
    api = Api(app, version='1.0.0', title='SoundSphere', description='A collection of shared records.')
    api.add_namespace(album_api)

    return app
