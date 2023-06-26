#!/bin/bash
docker-compose build

docker-compose up -d

docker exec consul-server1 /bin/sh -c "echo '{\"services\": [' >> /consul/config/counting.json"
while read line; do
  name=$(echo $line | cut -d ' ' -f 1)
  port=$(echo $line | cut -d ' ' -f 2)
  clust=$(echo $line | cut -d ' ' -f 3)
  data=$(echo $line | cut -d ' ' -f 4)
  echo $name
  echo $port
  echo $clust
  echo $data
  docker exec consul-server1 /bin/sh -c "echo '{\"name\": \"${name}\", \"tags\": [\"${clust}\", \"${data}\"], \"Address\": \"${name}\", \"port\": ${port}},' >> /consul/config/counting.json"
done
docker exec consul-server1 sed -i '$ s/.$//' /consul/config/counting.json
docker exec consul-server1 /bin/sh -c "echo ']}' >> /consul/config/counting.json"
docker exec consul-server1 consul reload
