#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
	echo "RUNNING IN DEVELOPMENT SERVER"
	exec python "identidock.py"
else 
	echo "RUNNING IN PRODUCTION SERVER"
	exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/identidock.py \
		--callable app --stats 0.0.0.0:9191
fi
