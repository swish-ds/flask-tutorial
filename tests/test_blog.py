import pytest
import json

test_post = {
    "title": "Test post title",
    "body": "Test post text"
}

test_post2 = {
    "title": "Test post title2",
    "body": "Test post text2"
}

test_post_put = {
    "title": "Updated post title",
    "body": "Updated post text"
}


def test_create(client, app):
    response = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."


def test_get_by_id(client, app):
    response_post = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_post.data.decode())
    assert response_post.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."

    response_get = client.get('/api/v1/posts/1')
    data = json.loads(response_get.data.decode())
    assert response_get.status_code == 200
    assert data['Post']['id'] == 1
    assert data['Post']['title'] == test_post['title']
    assert data['Post']['body'] == test_post['body']


def test_get_all(client, app):
    response_post = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_post.data.decode())
    assert response_post.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."

    response_post = client.post('/api/v1/posts',
                        data=json.dumps(test_post2),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_post.data.decode())
    assert response_post.status_code == 200
    assert data['Result'] == f"Post '{test_post2['title']}' created."

    response_get = client.get('/api/v1/posts')
    data = json.loads(response_get.data.decode())
    assert response_get.status_code == 200
    assert len(data['posts']) == 2
    assert data['posts'][0]['id'] == 1
    assert data['posts'][0]['title'] == test_post['title']
    assert data['posts'][0]['body'] == test_post['body']
    assert data['posts'][1]['id'] == 2
    assert data['posts'][1]['title'] == test_post2['title']
    assert data['posts'][1]['body'] == test_post2['body']


def test_update(client, app):
    response_post = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_post.data.decode())
    assert response_post.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."

    response_put = client.put('/api/v1/posts/1',
                        data=json.dumps(test_post_put),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_put.data.decode())
    assert data['Result'] == f"Post '{test_post_put['title']}' updated."


def test_delete(client, app):
    response_post = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_post.data.decode())
    assert response_post.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."

    response_delete = client.delete('/api/v1/posts/1',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response_delete.data.decode())
    assert response_delete.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' deleted."

    response_get = client.get('/api/v1/posts/1')
    assert response_get.status_code == 404


def test_create_error(client, app):
    response = client.post('/api/v1/posts',
                        data='post',
                        headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_update_error(client, app):
    response = client.post('/api/v1/posts',
                        data=json.dumps(test_post),
                        headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['Result'] == f"Post '{test_post['title']}' created."

    response_put = client.put('/api/v1/posts/1',
                        data='post',
                        headers={'Content-Type': 'application/json'})
    assert response_put.status_code == 400

