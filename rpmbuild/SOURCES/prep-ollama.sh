#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
spec_file="$script_dir/../SPECS/ollama.spec"

VERSION="${1:-${VERSION:-$(awk '
  /^%global[[:space:]]+upstream_version[[:space:]]+/ { print $3; found=1; exit }
  /^Version:[[:space:]]+/ && !found { print $2; exit }
' "$spec_file")}}"

test -n "$VERSION"

export GOAMD64="${GOAMD64:-v2}"

cd "$script_dir"

rm -f "ollama-${VERSION}-vendor.tar.gz"
rm -f "ollama-${VERSION}.tar.gz"
rm -f "v${VERSION}.tar.gz"
rm -rf "ollama-${VERSION}"

wget -O "v${VERSION}.tar.gz" "https://github.com/ollama/ollama/archive/refs/tags/v${VERSION}.tar.gz"
tar -zxf "v${VERSION}.tar.gz"
tar -zcf "ollama-${VERSION}.tar.gz" "ollama-${VERSION}"

pushd "ollama-${VERSION}" >/dev/null
go mod vendor
tar -zcf "../ollama-${VERSION}-vendor.tar.gz" vendor
popd >/dev/null

rm -rf "ollama-${VERSION}"
rm -f "v${VERSION}.tar.gz"
