#!/bin/sh
# wait-for-webserver.sh

set -e
  
cmd="$@"

until curl www1 && curl www2 && curl www3 && curl www4 && curl www5 && curl www6; do
  >&2 echo "Webserver are unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Webserver are up - executing command"
exec $cmd
