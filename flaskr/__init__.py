# contains the application factory
# tells Python that the flaskr directory should be treated as a package
import os
import app_config


from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import jinja2


db = SQLAlchemy()
migrate = Migrate()


def datetime_format(value):
    return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')


jinja2.filters.FILTERS["datetime_format"] = datetime_format


def init_app(app):
    # init_app prepares the application to work with SQLAlchemy. 
    # However that does not now bind the SQLAlchemy object to your application. 
    # Because there might be more than one application created.
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # configuration files are relative to the instance folder located outside the flaskr package

    # app.config.from_mapping(
    #     SECRET_KEY='dev', # used by Flask and extensions to keep data safe
    #     # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # ) # some default configuration

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(app_config.Config)
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        # return 'Hello, World!'
        return current_app.config['SQLALCHEMY_DATABASE_URI']

    from . import blog
    # add_url_rule() associates the endpoint name 'index' with the "/"" url
    # url_for('index') or url_for('blog.index') will both work, generating the same "/" URL
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from .api.v1 import bp as api_bp
    app.register_blueprint(api_bp , url_prefix='/api/v1')

    return app

from flaskr.models import ainfs
