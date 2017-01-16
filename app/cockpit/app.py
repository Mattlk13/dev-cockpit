import os
from flask import Flask, url_for
from celery import Celery
import celery.states as states
import redis

from views.start_page import start_page
from views.app_page import app_page
from common import datastore

env=os.environ

app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])

app.register_blueprint(start_page)
app.register_blueprint(app_page)

'''
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL','redis://127.0.0.1:6379'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND','redis://localhost:6379')
'''

if 'PYCHARM_HOSTED' in os.environ.keys():
    celery = Celery('tasks', broker='redis://127.0.0.1:7379/0', backend='redis://127.0.0.1:7379/0')
else:
    celery = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://dev-cockpit-redis:6379/0')

@app.route('/add/<int:param1>/<int:param2>')
def add(param1,param2):
    task = celery.send_task('mytasks.add', args=[param1, param2], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                url=url_for('check_task',id=task.id,_external=True))

repostore = redis.StrictRedis(host='127.0.0.1', port=6379, db=10, charset="utf-8", decode_responses=True)


redis = redis.StrictRedis(host='127.0.0.1', port=7379, db=10, charset="utf-8", decode_responses=True)



repokeys = redis.zrangebylex('repos', '-', '+')
for k in repokeys:
    name = redis.hget('repohash', k)
    if name.startswith("bibbox/app-"):
        command = "cd ../../data/bibboxgithub; git clone https://github.com/" + name + ".git"
        print(command)
        #os.system(command)
    if name.startswith("bibbox/sys-"):
        command = "cd ../../data/bibboxgithub; git clone https://github.com/" + name + ".git"
        print(command)
        #os.system(command)

print(os.listdir('../../data/bibboxgithub'))
os.system("cd ../../data/bibboxgithub; ls -la")



@app.route('/git')
def git():
    task = celery.send_task('mytasks.getGithub', args=[], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                    url=url_for('check_task', id=task.id, _external=True))


@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    if res.state==states.PENDING:
        return res.state
    else:
        return str(res.result)




'''
for repo in g.get_user().get_repos():
    rkey = "repo:" + repo.name.lower()
    print(rkey, " - ", repo.name)
    redis.zadd("repos", 0, rkey)
    redis.hset('repohash', rkey, repo.name)
allrepositories = []
allr = ''
'''

if __name__ == '__main__':
    app.run()