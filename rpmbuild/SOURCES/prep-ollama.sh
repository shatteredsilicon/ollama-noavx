#!/bin/bash

set -e

export GOAMD64=v2

VERSION="0.6.8"

rm -f ollama-${VERSION}-vendor.tar.gz
rm -f ollama-${VERSION}.tar.gz
rm -f v${VERSION}.tar.gz

wget https://github.com/ollama/ollama/archive/refs/tags/v${VERSION}.tar.gz
tar -zxvf v${VERSION}.tar.gz
tar -zcvf ollama-${VERSION}.tar.gz ollama-${VERSION}

pushd ollama-${VERSION}
go mod vendor
tar -zcvf ../ollama-${VERSION}-vendor.tar.gz vendor
popd

rm -rf ollama-${VERSION}
rm -f v${VERSION}.tar.gz
