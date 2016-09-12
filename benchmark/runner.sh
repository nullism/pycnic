#!/bin/bash

output="Test results:\n"

for app in bobo_test falcon_test pycnic_test cherrypy_test pyramid_test hug_test flask_test bottle_test tornado_test;
do
    echo "TEST: $app"
    if [ "$app" = "tornado_test" ]; then
	worker="tornado"
    else
	worker="sync"
    fi
    gunicorn -w 3 -k $worker $app:app &
    gunicorn_pid=$!
    sleep 2
    ab_out=`ab -n 5000 -c 5 http://127.0.0.1:8000/json`
    kill $gunicorn_pid
    rps=`echo "$ab_out" | grep "Requests per second"`
    crs=`echo "$ab_out" | grep "Complete requests"`
    output="$output\n$app:\n\t$rps\n\t$crs"
done

echo -e "$output"
