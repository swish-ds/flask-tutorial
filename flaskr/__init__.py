# contains the application factory
# tells Python that the flaskr directory should be treated as a package
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # configuration files are relative to the instance folder located outside the flaskr package
    app.config.from_mapping(
        SECRET_KEY='dev', # used by Flask and extensions to keep data safe
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    ) # some default configuration

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    # add_url_rule() associates the endpoint name 'index' with the "/"" url
    # url_for('index') or url_for('blog.index') will both work, generating the same "/" URL
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
