from flaskr.api.v1 import bp
from flask import jsonify, request
from flaskr.api.v1.celery.celery_tasks import long_task
from flask import url_for

@bp.route('/longtask', methods=['PUT'])
def run_longtask():
    task = long_task.apply_async()

    return jsonify({"taskID": task.id}), 202, {'Location': url_for('blog.taskstatus', task_id = task.id)}
