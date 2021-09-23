from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.models.ainfs import Post

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

