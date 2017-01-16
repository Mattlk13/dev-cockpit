from flask import g
import os
from github import Github

def init(app):
    """ Function must be called to initalize this module """

    global _db_config
    global close_connection

def _github():
    try:
        return Github("lomadi", "loibach99")
    except:
        print ("ERROR cannot conenct to github")
        raise

def get_github():
    github  = getattr(g, '_github', None)
    if github is None:
        github = g._github= _github()
    return github

def close_connection(exception):
    github = getattr(g, '_github', None)
    if github is not None:
# TODO close and cleanup redis connection, is there anything to do
        print ("Close the connection")