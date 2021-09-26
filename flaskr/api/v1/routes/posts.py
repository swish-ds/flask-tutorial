from flaskr import db
from flaskr.models.ainfs import Post
from flaskr.api.v1 import bp
from flask import jsonify, request, Response


@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.id)
    results = {"posts": [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at
        } for post in posts]
    }

    return jsonify(results)


@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(title=data['title'], body=data['body'])
    db.session.add(new_post)
    db.session.commit()
    results = {
        "Result": f"Post '{new_post.title}' created."
    }
    return jsonify(results)


@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    results = {
        "Post": {
            "id": post.id,
            "title": post.title,
            "body": post.body
        }
    }

    return jsonify(results)


@bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.body = data['body']
    db.session.add(post)
    db.session.commit()
    results = {
        "Result": f"Post '{post.title}' updated."
    }

    return jsonify(results)


@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    results = {
        "Result": f"Post '{post.title}' deleted."
    }
    

    return jsonify(results)
