#!/bin/sh

OPTS="--dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151" 
export LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib
export CXX=/home/grafik/gcc-modules/bin/g++-mxx
#python ./parallel_perf.py ${OPTS} --jobs=8 --json-out=data/gcc135-150-j008-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=16 --json-out=data/gcc135-150-j016-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=32 --json-out=data/gcc135-150-j032-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=48 --json-out=data/gcc135-150-j048-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=64 --json-out=data/gcc135-150-j064-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=80 --json-out=data/gcc135-150-j080-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=96 --json-out=data/gcc135-150-j096-gcc.json --toolset=gcc
#python ./parallel_perf.py ${OPTS} --jobs=128 --json-out=data/gcc135-150-j128-gcc.json --toolset=gcc
export LD_LIBRARY_PATH=/home/grafik/clang/lib
export CXX=/home/grafik/clang/bin/clang
#python ./parallel_perf.py ${OPTS} --jobs=8 --json-out=data/gcc135-150-j008-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=16 --json-out=data/gcc135-150-j016-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=32 --json-out=data/gcc135-150-j032-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=48 --json-out=data/gcc135-150-j048-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=64 --json-out=data/gcc135-150-j064-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=80 --json-out=data/gcc135-150-j080-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=96 --json-out=data/gcc135-150-j096-clang.json --toolset=clang
#python ./parallel_perf.py ${OPTS} --jobs=128 --json-out=data/gcc135-150-j128-clang.json --toolset=clang

OPTS="--dir=/home/grafik/temp/cpp_stats --def-ints --jobs=128 --json-out=/home/grafik/temp/cpp_stats/data.json --toolset=clang --run-samples=1"
#python ./parallel_perf.py ${OPTS} --exec-stats=data/gcc135-150-j128-d020-clang-stat-modules.json --dag-depth=20 --kind=modules
#python ./parallel_perf.py ${OPTS} --exec-stats=data/gcc135-150-j128-d020-clang-stat-headers.json --dag-depth=20 --kind=headers
python ./parallel_perf.py ${OPTS} --exec-stats=data/gcc135-150-j128-d100-clang-stat-modules.json --dag-depth=100 --kind=modules
python ./parallel_perf.py ${OPTS} --exec-stats=data/gcc135-150-j128-d100-clang-stat-headers.json --dag-depth=100 --kind=headers
