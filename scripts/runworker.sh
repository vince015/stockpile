#!/bin/bash
set -e  # exit on error
. /home/matthew/src/stockpile/env/bin/activate
exec python3 /home/matthew/src/stockpile/manage.py runworker