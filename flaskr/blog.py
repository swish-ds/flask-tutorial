from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.models.ainfs import Post

bp = Blueprint('blog', __name__)


@bp.route('/posts')
def get_posts():
    posts = Post.query.all()
    results = {"posts": [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at
        } for post in posts]
    }

    return results


@bp.route('/')
def index():
    results = get_posts()

    return render_template('blog/index.html', results=results)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        # if request.is_json:
        # data = request.get_json()
        title = request.form['title']
        body = request.form['body']
        # new_post = Post(title=data['title'], body=data['body'])
        new_post = Post(title=title, body=body)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.index'))
        # else:
        #     return {"error": "The request payload is not in JSON format"}

    return render_template('blog/create.html')



@bp.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)

    response = {
        "title": post.title,
        "body": post.body
    }
    return {"post": response}


@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get_or_404(post_id)

    # if request.method == 'PUT':
    if request.method == 'POST':
        # data = request.get_json()
        title = request.form['title']
        body = request.form['body']
        # post.title = data['title']
        # post.body = data['body']
        post.title = title
        post.body = body
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.index'))

        # return {"message": f"Post {post.title} successfully updated"}
    
    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
    # return {"message": f"Post {post.title} successfully deleted."}
