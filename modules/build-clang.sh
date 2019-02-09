#!/bin/sh

export JOBS=${JOBS:=8}
export CC=${CC:=gcc}
export CXX=${CXX:=g++}
export CMAKE=${CMAKE:=cmake}


PREFIX=`pwd`
ROOT=${PREFIX}/__build__
export TEMP=${PREFIX}/__temp__
export LD_LIBRARY_PATH=${PREFIX}/lib

set -e
mkdir -p ${ROOT}
pushd ${ROOT}
mkdir -p ${TEMP}

rm -rf include lib share

rm -f ./makeinfo
ln -s /usr/bin/true makeinfo
export PATH=${PWD}:${PATH}
export MAKEINFO=true

rm -rf llvm-7.0.1.src cfe-7.0.1.src
curl -L http://releases.llvm.org/7.0.1/llvm-7.0.1.src.tar.xz | tar xfJ -
curl -L http://releases.llvm.org/7.0.1/cfe-7.0.1.src.tar.xz | tar xfJ -
ln -s cfe-7.0.1.src clang

pushd llvm-7.0.1.src
mkdir __build__
cd __build__
${CMAKE} \
-DCMAKE_BUILD_TYPE=Release \
-DLLVM_INCLUDE_EXAMPLES=OFF \
-DLLVM_BUILD_TESTS=OFF \
-DLLVM_INCLUDE_TESTS=OFF \
-DLLVM_ENABLE_PROJECTS=clang \
-DBUILD_SHARED_LIBS=OFF \
-DCMAKE_INSTALL_PREFIX=${PREFIX} \
-G "Unix Makefiles" ..
make -j ${JOBS}
make install-strip
popd
rm -rf llvm-7.0.1.src cfe-7.0.1.src

popd
