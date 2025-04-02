#!/bin/bash

set -e

export GOAMD64=v2

VERSION="0.6.2"

rm -f ollama-${VERSION}-vendor.tar*
rm -f ollama-${VERSION}.tar*

wget https://github.com/ollama/ollama/archive/refs/tags/v${VERSION}.tar.gz
tar -zxvf v${VERSION}.tar.gz
tar -zcvf ollama-${VERSION}.tar.gz ollama-${VERSION}

cp golang-version.patch ollama-${VERSION}/
pushd ollama-${VERSION}
patch -p1 < golang-version.patch
go mod vendor
tar -zcvf ../ollama-${VERSION}-vendor.tar.gz vendor
popd

rm -rf ollama-${VERSION}
rm -f v${VERSION}.tar.gz
