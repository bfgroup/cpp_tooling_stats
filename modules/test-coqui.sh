#!/bin/sh

export CXX=/Developer/Tools/gcc-modules/bin/g++-mxx
./parallel_perf.py --dir=${HOME}/devcache/cpp_stats --def-ints --dag-depth=1,151 --jobs=8 --toolset=gcc --json-out=data/coqui-150-j008-gcc.json

export CXX=/Users/grafik/devcache/clang-7/bin/clang
./parallel_perf.py --dir=${HOME}/devcache/cpp_stats --def-ints --dag-depth=1,151 --jobs=8 --toolset=clang --json-out=data/coqui-150-j008-clang.json

export CXX=/Users/grafik/devcache/clang-7/bin/clang
OPTS="--dir=${HOME}/devcache/cpp_stats --def-ints --jobs=8 --json-out=${HOME}/devcache/cpp_stats/data.json --toolset=clang --run-samples=1"
python ./parallel_perf.py ${OPTS} --exec-stats=data/coqui-150-j008-d020-clang-stat-modules.json --dag-depth=20 --kind=modules
python ./parallel_perf.py ${OPTS} --exec-stats=data/coqui-150-j008-d020-clang-stat-headers.json --dag-depth=20 --kind=headers
