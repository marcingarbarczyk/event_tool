#!/bin/bash
PORT=${1:-8000}
mkdir -p /logs/event_tool/gunicorn
python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn -b 0.0.0.0:$PORT event_tool.wsgi:application -w 1 -t 300 --preload --access-logfile /logs/event_tool/gunicorn/access.log --capture-output --enable-stdio-inheritance --access-logformat '%({x-forwarded-for}i)s %(t)s %(l)s %(s)s "%(r)s" %(l)s %(a)s'
