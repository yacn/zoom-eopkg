#!/usr/bin/env bash

# as much as i'd like to use python, pyyaml doesn't preserve
# order or formatting (and truly that's beyond it's scope)
# which makes for some really really ugly package.ymls
# so instead we create more problems by updating package.yml with regex
# however we _can_ use python go get the values to update

function usage() { echo "$0 <version> <checksum> <release> < package.yml > whatever.yml"; exit; }

if [[ $# != 3 ]]; then
	usage
fi

version="$1"
checksum="$2"
release="$3"

sed "s/version: [0-9.]\+$/version: $version/" < /dev/stdin \
| sed "s/zoom_amd64.deb: [0-9a-z]\+$/zoom_amd64.deb: $checksum/" \
| sed "s/release: [0-9]\+$/release: $release/"
