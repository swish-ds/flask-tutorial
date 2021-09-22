from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.models.ainfs import Post

bp = Blueprint('blog', __name__)

@bp.route('/posts', methods=['POST', 'GET'])
def handle_posts():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_post = Post(title=data['title'], body=data['body'])
            db.session.add(new_post)
            db.session.commit()
            return {"message": f"Post {new_post.title} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        posts = Post.query.all()
        results = [
            {
                "title": post.title,
                "body": post.body
            } for post in posts]

        return {"count": len(results), "posts": results}


@bp.route('/posts/<post_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'GET':
        response = {
            "title": post.title,
            "body": post.body
        }
        return {"message": "success", "post": response}

    elif request.method == 'PUT':
        data = request.get_json()
        post.title = data['title']
        post.body = data['body']
        db.session.add(post)
        db.session.commit()
        return {"message": f"Post {post.title} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return {"message": f"Post {post.title} successfully deleted."}







@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created'
        ' FROM post p'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body)'
                ' VALUES (?, ?)',
                (title, body)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created'
        ' FROM post p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
# update function takes an argument, id. That corresponds to the <int:id> in the route
# if a real URL is /1/update Flask will capture the 1, ensure it’s an int, and pass it as the id argument.
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

