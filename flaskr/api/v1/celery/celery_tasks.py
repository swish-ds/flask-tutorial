from flaskr import celery, db
import time
import random
from celery.utils.log import get_task_logger
from flaskr.models.ainfs import Post

logger = get_task_logger(__name__)


def add_to_db(title, body):
    new_post = Post(title=title, body=body)
    db.session.add(new_post)
    db.session.commit()
    logger.info(f'Successfully inserted post "{title}"')


@celery.task(bind=True)
def long_task2(self, title, body):
    total = random.randint(5, 10)
    for i in range(total):
        logger.info(f'Insert in {total - i} seconds')
        time.sleep(1)
    logger.info(f'Insert post into the database')
    add_to_db(title, body)




# @celery.task(bind=True)
# def long_task(self):
#     """Background task that runs a long function with progress reports."""
#     verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
#     adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
#     noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
#     message = ''
#     total = random.randint(5, 10)
#     for i in range(total):
#         logger.info(f'***** ITERATION #{i} *****')
#         if not message or random.random() < 0.25:
#             message = '{0} {1} {2}...'.format(random.choice(verb),
#                                               random.choice(adjective),
#                                               random.choice(noun))
#         self.update_state(state='PROGRESS',
#                           meta={'current': i, 'total': total,
#                                 'status': message})
#         time.sleep(1)
#     return {'current': 100, 'total': 100, 'status': 'Task completed!',
#             'result': 42}
