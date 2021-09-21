# contains setup functions called fixtures that each test will use
# Each test will create a new temporary database file and populate some data that will be used in the tests. (tests/data.sql)

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # will call the factory and pass test_config to configure the application and database for testing
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # After setting the path, the database tables are created and the test data is inserted
    # Each test will create a new temporary database file and populate some data that will be used in the tests.
    with app.app_context():
        # everything that runs in the block will have access to current_app.
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # After the test is over, the temporary file is closed and removed.
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # creates a runner that can call the Click commands registered with the application.
    return app.test_cli_runner()


# For most of the views, a user needs to be logged in. 
# way to do this is to make a POST request to the login view with the client.
class AuthActions(object):
    # class with methods to do that, and use a fixture to pass it the client for each test.
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    # call auth.login() in a test to log in as the test user, which was inserted as part of the test data in the app fixture.
    return AuthActions(client)