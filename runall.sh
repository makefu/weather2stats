#! /bin/sh
(while sleep 15m; do python3 stadtklima-stuttgart.py ; echo "`date`: done"; done)&
(while sleep 30m; do python3 openweathermap.py; echo "`date`:done" ;done)&
(while sleep 30m; do python3 opensensemap.py ;echo "`date`:done" ; done)&
echo "waiting for all"
wait
