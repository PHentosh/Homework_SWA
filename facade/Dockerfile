FROM python:latest
COPY ./requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt
COPY ./front_page.py /opt/app/
ENTRYPOINT ["python", "-u", "/opt/app/front_page.py"]