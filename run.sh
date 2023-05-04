#!/bin/bash

python challenge.py &
python genKeys.js &
python mempool.py &
python nonce.py &
python oracle.py &
python pubSub.py &

wait
