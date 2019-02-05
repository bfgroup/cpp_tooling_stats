#!/bin/sh

./parallel_perf.py --dir=${HOME}/devcache/cpp_stats --def-ints --dag-depth=1,151 --jobs=8 --json-out=data/coqui-150-j008.json
./parallel_perf.py --dir=${HOME}/devcache/cpp_stats --def-ints --dag-depth=1,151 --jobs=8 --json-out=data/coqui-150-j008-mm.json --use-mapper-file
