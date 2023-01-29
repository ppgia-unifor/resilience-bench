FROM python:3.9

WORKDIR /opt/app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD ./scheduler .

CMD ["python", "-u", "app.py"]