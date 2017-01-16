from common import github_connection
from common import datastore

g = github_connection.get_github()
for repo in g.get_user().get_repos():
    rkey = "repo:" + repo.name.lower()
    print(rkey, " - ", repo.name)

    redis.zadd("repos", 0, rkey)
    redis.hset('repohash', rkey, repo.name)
