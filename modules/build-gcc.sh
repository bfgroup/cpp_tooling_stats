#!/bin/sh

JOBS=8
PREFIX=`pwd`
ROOT=${PREFIX}/__build__

set -e
mkdir -p ${BUILD}
pushd ${BUILD}

export CC=gcc-7
export CXX=g++-7

rm -rf include lib share

rm -f ./makeinfo
ln -s /usr/bin/true makeinfo
export PATH=${PWD}:${PATH}
export MAKEINFO=true
rm -rf gmp-6.1.0 mpfr-3.1.4 mpc-1.0.3 isl-0.18
curl -L ftp://gcc.gnu.org/pub/gcc/infrastructure/gmp-6.1.0.tar.bz2 | tar xf -
curl -L ftp://gcc.gnu.org/pub/gcc/infrastructure/mpfr-3.1.4.tar.bz2 | tar xf -
curl -L ftp://gcc.gnu.org/pub/gcc/infrastructure/mpc-1.0.3.tar.gz | tar xf -
curl -L ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-0.18.tar.bz2 | tar xf -

pushd gmp-6.1.0
mkdir __build__
cd __build__
../configure --prefix=${PREFIX} --enable-cxx
make -j ${JOBS}
make install-strip
popd
rm -rf gmp-6.1.0

pushd mpfr-3.1.4
mkdir __build__
cd __build__
../configure --prefix=${PREFIX} --with-gmp=${PREFIX}
make -j ${JOBS}
make install-strip
popd
rm -rf mpfr-3.1.4

pushd mpc-1.0.3
mkdir __build__
cd __build__
../configure --prefix=${PREFIX} --with-gmp=${PREFIX} --with-mpfr=${PREFIX}
make -j ${JOBS}
make install-strip
popd
rm -rf mpc-1.0.3

pushd isl-0.18
mkdir __build__
cd __build__
../configure --prefix=${PREFIX} --with-gmp-prefix=${PREFIX}
make -j ${JOBS}
make install-strip
popd
rm -rf isl-0.18

rm -rf gcc-svn
svn co svn://gcc.gnu.org/svn/gcc/branches/c++-modules gcc-svn
pushd gcc-svn
svn up
rm -rf __build__
mkdir __build__
cd __build__
../configure \
--prefix=${PREFIX} \
--with-gmp=${PREFIX} \
--with-mpfr=${PREFIX} \
--with-mpc=${PREFIX} \
--with-isl=${PREFIX} \
--program-suffix=-mxx \
--enable-checking=release \
--enable-languages=c,c++ \

make -j ${JOBS}
make install-strip
cd ..
rm -rf __build__

popd
