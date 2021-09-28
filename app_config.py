import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost:5432/flask_tutorial'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    worker_redirect_stdouts_level = "INFO"
    task_ignore_result = False
    accept_content = ['application/json']
    result_serializer = 'json'
    task_serializer = 'json'
    task_track_started = True
    worker_redirect_stdouts = True
    worker_send_task_events = True
    task_send_sent_event = True
    worker_hijack_root_logger = False
