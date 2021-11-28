FROM python:3.9

RUN useradd -ms /bin/bash app
USER app
WORKDIR /opt/orchestrator
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .

CMD ["python", "app.py"]