FROM envoyproxy/envoy:v1.36.12 AS envoy

FROM ubuntu:24.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-venv supervisor ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=envoy /usr/local/bin/envoy /usr/local/bin/envoy

# httpbin: the maintained PyPI release (psf/httpbin) supports current Python and ships wheels for amd64 and arm64
RUN python3 -m venv /opt/httpbin && \
    /opt/httpbin/bin/pip install --no-cache-dir httpbin==0.10.4 gunicorn==23.0.0 gevent==24.11.1
ENV PATH="/opt/httpbin/bin:${PATH}"

RUN mkdir -p /var/log/envoy

ADD envoy.yaml /etc/envoy/envoy.yaml
ADD supervisord.conf /etc/supervisor/conf.d/default.conf

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/default.conf" ]
