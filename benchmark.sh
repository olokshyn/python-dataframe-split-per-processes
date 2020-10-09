#!/bin/bash

params="--proc-num 4 --no-limits"

mprof run python multiprocessing_as_argument.py $params
mprof plot &
sleep 10
mprof run python multiprocessing_as_global.py $params
mprof plot &
