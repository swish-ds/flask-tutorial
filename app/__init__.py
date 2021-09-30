# contains the application factory
# tells Python that the flaskr directory should be treated as a package
import os
import app_config
import jinja2

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
db_session = None

celery = Celery(__name__)
# celery = Celery(__name__, broker=app_config.Config.CELERY_BROKER_URL, backend=app_config.Config.CELERY_RESULT_BACKEND)


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


def make_celery(app):
    celery.config_from_object(app_config.Config)

    TaskBase = celery.Task

    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            if not celery.conf.task_always_eager:
                with app.app_context():
                    db.session.remove()
                    db.session.close_all()  # noqa # pylint: disable=E1101
                    db.engine.dispose()

                    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
                    db_sess = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
                    db.session = db_sess

                    return TaskBase.__call__(self, *args, **kwargs)
            else:
                # db.session = db_session
                return TaskBase.__call__(self, *args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            """
            After each Celery task, teardown our db session.
            """
            if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] and not isinstance(retval, Exception):
                db.session.commit()  # noqa
            # If we aren't in an eager request (i.e. Flask will perform teardown), then teardown
            if not celery.conf.CELERY_ALWAYS_EAGER:
                db.session.remove()

            # # Clean folders
            # local_dirs = (os.path.join(app.config.get('ARTI_PROJECTS_DIR_PATH'), task_id),
            #               os.path.join(app.config.get('GIT_PROJECTS_DIR_PATH'), task_id))
            # for local_dir in local_dirs:
            #     if os.path.exists(local_dir):
            #         remove_folders_from_path(local_dir)

    celery.Task = ContextTask

    return celery

# def make_celery(app):
#     celery.config_from_object(app_config.Config)
#     TaskBase = celery.Task

#     class ContextTask(TaskBase):
#         abstract = True

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)

#     celery.Task = ContextTask

#     return celery


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(app_config.Config)
    else:
        app.config.from_object(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)


    @app.route('/hello')
    def hello():
        # return 'Hello, World!'
        return current_app.config['SQLALCHEMY_DATABASE_URI']

    # make_celery(app)

    from . import blog
    # add_url_rule() associates the endpoint name 'index' with the "/"" url
    # url_for('index') or url_for('blog.index') will both work, generating the same "/" URL
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # make_celery(app)

    from flaskr.api.v1 import bp as api_bp
    app.register_blueprint(api_bp , url_prefix='/api/v1')

    make_celery(app)

    # celery.config_from_object(app_config.Config)

    return app

# from flaskr.models import ainfs
# from flaskr.api.v1.celery.celery_tasks import long_task

# celery -A flaskr.celery worker --loglevel=info
# celery -A celery_worker.celery worker --loglevel=info
# celery -A celery_worker.celery worker -l info -E
