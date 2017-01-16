#!/bin/bash
set -e

export C_FORCE_ROOT=true

cd /celery-tasks
celery -A tasks worker --loglevel=INFO