import os
import time
from celery import Celery
import redis
from github import Github


env=os.environ

CELERY_BROKER_URL=env.get('CELERY_BROKER_URL','redis://localhost:6379'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND','redis://localhost:6379')

celery = Celery('tasks', broker='redis://dev-cockpit-redis:6379/0', backend='redis://dev-cockpit-redis:6379/1')

'''
if 'PYCHARM_HOSTED' in os.environ.keys():

else:
    celery = Celery('tasks', broker='redis://:bibbox4ever@127.0.0.1:6379/0', backend='redis://:bibbox4ever@dev-cockpit-redis:6379/0')
'''

print ("celery is connected")


@celery.task(name='mytasks.add')
def add(x, y):
    print ("I have to add someting")
    time.sleep(5) # lets sleep for a while before doing the gigantic addition task!
    return 10*(x + y)


@celery.task(bind=True, name='mytasks.getGithub')
def getGithub(self):
    g = Github("lomadi", "loibach99")
    repos = g.get_user().get_repos()
    rs = redis.StrictRedis(host='dev-cockpit-redis', port=6379, db=10, charset="utf-8", decode_responses=True)
    for repo in repos:
        rkey = "repo:" + repo.full_name.lower()
        print(rkey, " XX ", repo.full_name)
        rs.zadd("repos", 0, rkey)
        rs.hset('repohash:full_name', rkey, repo.full_name)
        rs.hset('repohash:name',      rkey, repo.full_name)

    return repos

