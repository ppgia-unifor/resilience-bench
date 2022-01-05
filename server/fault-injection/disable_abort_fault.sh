#!/usr/bin/env bash
set -e

[ -e /srv/runtime/v1/envoy/fault/http/abort/abort_percent ] && rm /srv/runtime/v1/envoy/fault/http/abort/abort_percent
[ -e /srv/runtime/v1/envoy/fault/http/abort/http_status ] && rm /srv/runtime/v1/envoy/fault/http/abort/http_status

pushd /srv/runtime
ln -s /srv/runtime/v1 new && mv -Tf new current
popd