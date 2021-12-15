FROM python:3.9

WORKDIR /opt/orchestrator
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .

CMD ["python", "-u", "app.py"]