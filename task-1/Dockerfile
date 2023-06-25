FROM python:latest
RUN pip install hazelcast-python-client
COPY ./app_1.py /opt/app/
ENTRYPOINT ["python", "/opt/app/app_1.py"]
