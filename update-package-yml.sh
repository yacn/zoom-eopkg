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

sed -E "s/version(\s+)?: [0-9.]+$/version\1: $version/" < /dev/stdin \
| sed -E "s/zoom_amd64.deb : [0-9a-z]+$/zoom_amd64.deb : $checksum/" \
| sed -E "s/release(\s+)?: [0-9]+$/release\1: $release/"
