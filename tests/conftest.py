# contains setup functions called fixtures that each test will use

from app_config import Config

import pytest
from flaskr import create_app, db


class TestConfig(Config):
    TESTING = True

# scope = session ??
@pytest.fixture()
def app():
    # will call the factory and pass TestConfig to configure the application and database for testing
    # create_app() gives us an app object, but the imported db isn’t connected (it has no engine)
    app = create_app(TestConfig)

    #create an AppContext instalnce and bind context to it. The same as with app.app_context(): ... ?
    app_context = app.app_context()
    # DB engine gets populated.
    app_context.push()
    # db.drop_all()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture()
def client(app):
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture(scope='module')
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
