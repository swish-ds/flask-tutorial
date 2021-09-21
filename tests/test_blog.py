import pytest
from flaskr.db import get_db


def test_index(client):
    response = client.get('/')

    # subsequent requests from the client will be logged in as the test user.
    response = client.get('/')
    # index view should display information about the post that was added with the test data.
    assert b'test title' in response.data
    assert b'test\nbody' in response.data
    # When logged in as the author, there should be a link to edit the post.
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    'path', 
    ('/2/update', '/2/delete',)
)
def test_exists_required(client, path):
    # If a post with the given id doesn’t exist, update and delete should return 404 Not Found.
    assert client.post(path).status_code == 404


def test_create(client, app):
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        # When valid data is sent in a POST request, create should insert the new post data into the database
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, app):
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        # When valid data is sent in a POST request, update should modify the existing data.
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize(
    'path', 
    ('/create','/1/update',)
)
def test_create_update_validate(client, path):
    # Both pages should show an error message on invalid data.
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, app):
    # delete view should redirect to the index URL
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        # post should no longer exist in the database.
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

