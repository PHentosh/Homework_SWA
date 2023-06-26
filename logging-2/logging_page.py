from flask import Flask, request
import hazelcast
import requests
import json
import consulate
import time

time.sleep(30)
consul = consulate.Consul(host='consul-server1')

consul.agent.service.register('logging-2',
                               port=8084,
                               address='logging-2',
                               ttl='10s')

app = Flask(__name__)

services = json.loads(consul.agent.services())
mq = []
map_n = ""
clust_n = ""
for name in services.keys():
    if "hazelcast-2" in name:
        mq.append(services[name]['Address'])
        map_n = services[name]['Tags'][1]
        clust_n = services[name]['Tags'][0]


client = hazelcast.HazelcastClient(
cluster_name=clust_n, 
cluster_members=mq)


map_t = client.get_map(map_n).blocking()

@app.get('/')
def login_get():
    global map_t
    keys = map_t.key_set()
    all = map_t.get_all(keys)
    return str(all)

@app.post('/')
def login_post():
    global map_t
    mess = request.data
    print(str(mess)[2:-1])
    get_json = json.loads(str(mess)[2:-1].replace("\'", "\""))
    keys = list(get_json.keys())
    map_t.put(keys[0], get_json[keys[0]])
    return "message registered"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8084, debug=True)