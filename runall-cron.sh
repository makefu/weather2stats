#! /bin/sh
cd "$(dirname "$(readlink -f "$0")")"
. bin/activate
set -eufx
ret=0
if ! python3 stadtklima-stuttgart.py;then
  echo Stadtklima failed
  ret=1
fi
if ! python3 openweathermap.py;then
  echo Openweathermap failed
  ret=1
fi
if ! python3 opensensemap.py;then 
  echo opensensemap failed
  ret=1
fi

exit $ret
