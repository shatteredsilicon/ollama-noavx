#!/bin/bash

export GOAMD64=v2

rm -rf ollama ollama-0.5.7
rm -f ollama-0.5.7-git.tar*
rm -f ollama-0.5.7-vendor.tar*

rm -f ollama-0.5.7.tar.gz
wget -O ollama-0.5.7.tar.gz "https://github.com/ollama/ollama/archive/refs/tags/v0.5.7.tar.gz"

git clone https://github.com/ollama/ollama.git
mv ollama ollama-0.5.7
tar -cf ollama-0.5.7.tar ollama-0.5.7
pushd ollama-0.5.7
git checkout v0.5.7
popd
pushd ollama-0.5.7
git submodule init
git submodule update --force llama/llama.cpp
patch < ../golang-version.patch
go mod vendor
tar -cf ../ollama-0.5.7-git.tar .git*
tar -cf ../ollama-0.5.7-vendor.tar vendor
popd
rm -f ollama-0.5.7-git.tar.xz
rm -f ollama-0.5.7-vendor.tar.xz
pxz -9 ollama-0.5.7-git.tar
pxz -9 ollama-0.5.7-vendor.tar
