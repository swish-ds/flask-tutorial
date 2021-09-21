# The register view should render successfully on GET.
# On POST with valid form data, it should redirect to the login URL and the user’s data should be in the database.
# Invalid data should display error messages.

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    # headers will have a Location header with the login URL when the register view redirects to the login view. ( return redirect(url_for("auth.login")) )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


# parametrize tells Pytest to run the same test function with different arguments.
# to test different invalid input and error messages without writing the same code three times.
@pytest.mark.parametrize(
    ('username', 'password', 'message'), 
    (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
    )
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


# session should have user_id set after logging in.
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        # Using client in a with block allows accessing context variables such as session after the response is returned. 
        # Normally, accessing session outside of a request would raise an error.
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(
    ('username', 'password', 'message'), 
    (
        ('a', 'test', b'Incorrect username.'),
        ('test', 'a', b'Incorrect password.')
    )
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


# session should not contain user_id after logging out.
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
