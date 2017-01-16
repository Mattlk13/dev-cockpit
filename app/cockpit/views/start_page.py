from flask import Blueprint, render_template, abort, g
from jinja2 import TemplateNotFound
from github import Github
import json
import urllib.request as ur

from common import github_connection
from common import datastore


start_page = Blueprint('start_page', __name__, template_folder='templates')
@start_page.route('/')
def show():

    redis = datastore.get_datastore()

    repokeys = redis.zrangebylex('repos', '-', '+')
    allr = ''

    g = Github("f87f5f9e252e348b01b65018a6b2be49d88f12e1")

    #access_token = 'BLAH'
    #gh = Github(access_token, base_url='https://myorg.github.com/api/v3')
    #gh.get_user().name

    #class github.MainClass.Github(login_or_token=None, password=None, base_url='https://api.github.com', timeout=10, client_id=None, client_secret=None, user_agent='PyGithub/Python', per_page=30)¶

    user = g.get_user()


    repos = user.get_repos()
    for k in repokeys:
        name = redis.hget('repohash', k)
        if name.startswith("bibbox/app-"):
            try:
                r = g.get_repo(name)
#                file = r.get_file_contents("appinfo.json")
#                print("READ ", file.url)
#               desrc = json.loads( ur.urlopen(file.url).read().decode('utf8') )
#               print(desrc)

            except ZeroDivisionError as e:
                print("no appinfo")

    for k in repokeys:
        name = redis.hget('repohash', k)
        if name.startswith("bibbox/app-"):
            allr = allr + "<h3>" + str(name) + "</h3>"
        if name.startswith("sys-"):
            allr = allr + "<h3>" + str(name) + "</h3>"

    return allr
