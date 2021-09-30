from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr import db
from flaskr.models.ainfs import Post
from flaskr.api.v1.celery.celery_tasks import celery_insert

import requests
import json


url = 'http://127.0.0.1:5000'

bp = Blueprint('blog', __name__)

headers = {
    'Content-Type': 'application/json'
}


@bp.route('/')
def index():
    path = '/api/v1/posts'
    results = requests.request('GET', url + path)

    return render_template('blog/index.html', results=results.json())


@bp.route('/task', methods=('GET', 'POST'))
def celery_task():
    if request.method == 'POST':
        path = '/api/v1/longtask'
        title = request.form['title']
        body = request.form['body']
        payload = json.dumps({
        "title": title,
        "body": body
        })

        results = requests.request('PUT', url + path, headers=headers, data=payload)
        results = results.json()
        # return results.text

        return redirect(url_for('blog.taskstatus', task_id = results['taskID']))


    return render_template('blog/task.html')


@bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = celery_insert.AsyncResult(task_id)
    response = {
        'state': task.state,
        'status': str(task.info)
    }
    # if task.state == 'PENDING':
    #     response = {
    #         'state': task.state,
    #         'current': 0,
    #         'total': 1,
    #         'status': 'Pending...'
    #     }
    # elif task.state != 'FAILURE':
    #     response = {
    #         'state': task.state,
    #         'current': task.info.get('current', 0),
    #         'total': task.info.get('total', 1),
    #         'status': task.info.get('status', '')
    #     }
    #     if 'result' in task.info:
    #         response['result'] = task.info['result']
    # else:
    #     # something went wrong in the background job
    #     response = {
    #         'state': task.state,
    #         'current': 1,
    #         'total': 1,
    #         'status': str(task.info),  # this is the exception raised
    #     }
    return jsonify(response)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        path = '/api/v1/posts'
        title = request.form['title']
        body = request.form['body']

        payload = json.dumps({
        "title": title,
        "body": body
        })

        results = requests.request('POST', url + path, headers=headers, data=payload)

        return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        path = f'/api/v1/posts/{post_id}'
        title = request.form['title']
        body = request.form['body']

        payload = json.dumps({
        "title": title,
        "body": body
        })

        results = requests.request('PUT', url + path, headers=headers, data=payload)

        return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    path = f'/api/v1/posts/{post_id}'

    results = requests.request('DELETE', url + path)

    return redirect(url_for('blog.index'))

