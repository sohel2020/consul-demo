FROM python:2.7
MAINTAINER Tarikur Rahaman <tarikur@telenoehealth.com>
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
COPY app.py /
EXPOSE 8080
CMD ["python", "/app.py"]
