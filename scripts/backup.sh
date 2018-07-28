#!/bin/bash
set -e  # exit on error
if [ ! -d "/home/matthew/bak" ]; then
  mkdir /home/matthew/bak
fi
cd /home/matthew/src/stockpile
. /home/matthew/src/stockpile/env/bin/activate

DATE=$(date +%FT%T_%Z)
python /home/matthew/src/stockpile/manage.py dumpdata --indent 4 > "$DATE".json
