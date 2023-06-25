FROM python:latest
RUN pip install hazelcast-python-client
COPY ./app_3.py /opt/app/
ENTRYPOINT ["python", "-u", "/opt/app/app_3.py"]
