#!/bin/bash
set -e

cd /celery-tasks
flower -A tasks --port=5555 --broker='redis://dev-cockpit-redis:6379/0'