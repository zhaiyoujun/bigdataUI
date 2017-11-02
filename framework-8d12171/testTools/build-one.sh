#!/bin/sh

set -x

cd $(dirname $0)

dir=$1
op=$2

rm -rf tmp && mkdir tmp

cp -r $dir tmp/$op

cd tmp/
tar -zcf ../$dir.tar.gz $op
cd -
