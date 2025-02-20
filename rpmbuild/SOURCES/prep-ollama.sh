#!/bin/bash

set -e

export GOAMD64=v2

rm -rf ollama-0.5.11
rm -f v0.5.11.tar.gz
rm -f ollama-0.5.11-vendor.tar*
rm -f ollama-0.5.11.tar*

wget https://github.com/ollama/ollama/archive/refs/tags/v0.5.11.tar.gz
tar -zxvf v0.5.11.tar.gz
tar -zcvf ollama-0.5.11.tar.gz ollama-0.5.11

cp golang-version.patch ollama-0.5.11/
pushd ollama-0.5.11
patch -p1 < golang-version.patch
go mod vendor
tar -zcvf ../ollama-0.5.11-vendor.tar.gz vendor
popd
