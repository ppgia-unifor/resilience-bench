#!/usr/bin/env bash
set -e

[ -e /srv/runtime/v1/envoy/fault/http/delay/fixed_delay_percent ] && rm /srv/runtime/v1/envoy/fault/http/delay/fixed_delay_percent
[ -e /srv/runtime/v1/envoy/fault/http/delay/fixed_duration_ms ] && rm /srv/runtime/v1/envoy/fault/http/delay/fixed_duration_ms

pushd /srv/runtime
ln -s /srv/runtime/v1 new && mv -Tf new current
popd