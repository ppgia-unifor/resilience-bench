FROM envoyproxy/envoy-dev:25cc9ea48ba18930e1235dfb6a6a236d59c8b08a

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt update -y && apt install python3-pip git supervisor -y
RUN git clone https://github.com/postmanlabs/httpbin.git /opt/httpbin && \
    cd /opt/httpbin && \
    pip3 install gunicorn decorator brotlipy gevent Flask meinheld "werkzeug>=0.14.1" six flasgger pyyaml && \
    pip3 install --no-cache-dir /opt/httpbin

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/default.conf" ]