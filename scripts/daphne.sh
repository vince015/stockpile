#!/bin/bash
set -e  # exit on error
cd /home/matthew/src/stockpile
. /home/matthew/src/stockpile/env/bin/activate
exec daphne -b 0.0.0.0 -p 8080 stockpile.asgi:channel_layer