from flaskr.api.v1 import bp
from flask import jsonify, request
from flaskr.api.v1.celery.celery_tasks import long_task2
from flask import url_for

@bp.route('/longtask', methods=['PUT'])
def run_longtask():
    data = request.get_json()
    task = long_task2.apply_async([data['title'], data['body']])

    return jsonify({"taskID": task.id}), 202, {'Location': url_for('blog.taskstatus', task_id = task.id)}
