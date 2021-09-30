from app_config import Config
import pytest
from flaskr import create_app, db
from flaskr.api.v1.celery.celery_tasks import celery_insert
import json
from flaskr.models.ainfs import Post
import time

test_post = {
    "title": "Test post title",
    "body": "Test post text"
}

def test_celery_insert(celery_app, client):
    response_put = client.put('/api/v1/longtask',
                    data=json.dumps(test_post),
                    headers={'Content-Type': 'application/json'})
    assert response_put.status_code == 202
    response_get = client.get('/api/v1/posts/1')
    data = json.loads(response_get.data.decode())
    assert data['Post']['title'] == test_post['title']

    # post = Post.query.get_or_404(1)
    # assert post.title == test_post['title']
    # assert post.body == test_post['body']

    # task = celery_insert.apply_async([test_post['title'], test_post['body']])
    # task's type is <class 'celery.result.EagerResult'>
    # task = add.delay(1, 2)
    # assert task.get()["state"] == "SUCCESS"
    # assert task.get() == test_post['title']
    # post = Post.query.get_or_404(1)
    # assert post.title == test_post['title']
