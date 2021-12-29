#!/usr/bin/env bash
set -e

mkdir -p /srv/runtime/v1/envoy/fault/http/abort
echo $1 > /srv/runtime/v1/envoy/fault/http/abort/abort_percent
echo $2 > /srv/runtime/v1/envoy/fault/http/abort/http_status

pushd /srv/runtime
ln -s /srv/runtime/v1 new && mv -Tf new current
popd