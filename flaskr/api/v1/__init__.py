from flask import Blueprint

bp = Blueprint('api_v1', __name__)

from flaskr.api.v1.routes import posts  # noqa
