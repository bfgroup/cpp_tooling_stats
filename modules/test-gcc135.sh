#!/bin/sh

LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=16 --json-out=data/gcc135-150-j016.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=32 --json-out=data/gcc135-150-j032.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=48 --json-out=data/gcc135-150-j048.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=64 --json-out=data/gcc135-150-j064.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=80 --json-out=data/gcc135-150-j080.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=96 --json-out=data/gcc135-150-j096.json
LD_LIBRARY_PATH=/home/grafik/gcc-modules/lib64:/home/grafik/gcc-modules/lib CXX=/home/grafik/gcc-modules/bin/g++-mxx python ./parallel_perf.py --dir=/home/grafik/temp/cpp_stats --def-ints --dag-depth=1,151 --jobs=128 --json-out=data/gcc135-150-j128.json
