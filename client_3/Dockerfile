FROM python:latest
RUN pip install hazelcast-python-client
COPY ./app_2.py /opt/app/
ENTRYPOINT ["python", "-u", "/opt/app/app_2.py"]
