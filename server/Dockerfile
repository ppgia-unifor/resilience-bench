FROM envoyproxy/envoy-dev

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt update -y && apt install python3-pip git supervisor -y && pip3 install --no-cache-dir pipenv
RUN git clone https://github.com/postmanlabs/httpbin.git /opt/httpbin && \
    cd httpbin && \
    /bin/bash -c "pip3 install --no-cache-dir -r <(pipenv lock -r)" \
    pip3 install --no-cache-dir /opt/httpbin

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/default.conf" ]
