from flask import Flask, request
import hazelcast
import threading
import os
import consulate
import json
import time

time.sleep(30)

consul = consulate.Consul(host='consul-server1')

consul.agent.service.register('messages-2',
                               port=8083,
                               address='messages-2',
                               ttl='10s')


messages = []

def listener():
    global messages

    services = json.loads(consul.agent.services())
    mq = []
    qn = ""
    clust_n = ""
    for name in services.keys():
        if "queue" in name:
            mq.append(services[name]['Address'])
            qn = services[name]['Tags'][1]
            clust_n = services[name]['Tags'][0]


    client = hazelcast.HazelcastClient(
    cluster_name=clust_n, 
    cluster_members=mq)


    queue = client.get_queue(qn).blocking()
    while True:
        el = queue.take()
        if el is not None:
            print(f"Get message {el}")
            messages.append(el)

def rest_api():
    global messages
    app = Flask(__name__)

    @app.get('/')
    def login_get():
        return messages

    app.run(host="0.0.0.0", port=8083, debug=False)

t1 = threading.Thread(target=listener, name='t1')
t2 = threading.Thread(target=rest_api, name='t2')

# starting threads
t1.start()
t2.start()

# wait until all threads finish
t1.join()
t2.join()