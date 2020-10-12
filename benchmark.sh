#!/bin/bash

params="--proc-num 4 --no-limits"

./plot_memory_usage.sh python3 multiprocessing_as_argument.py $params > as_argument.log 2>&1
mv mem-graph.png memory-argument.png
sleep 10
./plot_memory_usage.sh python3 multiprocessing_as_global.py $params > as_global.log 2>&1
mv mem-graph.png memory-global.png
