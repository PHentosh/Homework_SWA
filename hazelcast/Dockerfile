FROM hazelcast/hazelcast:5.3.1
USER root
RUN rm -rf /opt/hazelcast/config/hazelcast.xml
RUN rm -rf /opt/hazelcast/config/hazelcast-docker.xml
COPY ./hazelcast.xml /opt/hazelcast/config/hazelcast.xml
COPY ./hazelcast-docker.xml /opt/hazelcast/config/hazelcast-docker.xml