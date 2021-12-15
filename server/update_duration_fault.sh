#!/usr/bin/env bash
set -e

mkdir -p /srv/runtime/v1/envoy/fault/http/delay
echo $1 > /srv/runtime/v1/envoy/fault/http/delay/fixed_duration_ms

pushd /srv/runtime
ln -s /srv/runtime/v1 new && mv -Tf new current
popd
