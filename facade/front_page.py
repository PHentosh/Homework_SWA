from flask import Flask, request
import requests
import uuid
import random
import hazelcast
import consulate
import json
import time

time.sleep(30)


consul = consulate.Consul(host='consul-server1')

consul.agent.service.register('facade',
                               port=8080,
                               address='facade-service',
                               ttl='10s')


app = Flask(__name__)



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

@app.route('/',methods = ['GET', 'POST'])
def login():
    global queue
    if request.method == 'POST':
      dat = str(request.data)[2:-1]
      u = str(uuid.uuid4().hex)
      log_json = {u:dat}
      services = json.loads(consul.agent.services())
      log_serv = []
      for name in services.keys():
         if "logging" in name:
            log_serv.append(name)
      ind = random.randint(0, len(log_serv)-1)
      logging = requests.post(f"http://{services[log_serv[ind]]['Address']}:{services[log_serv[ind]]['Port']}", data=str(log_json)).content
      queue.put(dat)
      return logging
    else:
      services = json.loads(consul.agent.services())
      log_serv = []
      for name in services.keys():
         if "logging" in name:
            log_serv.append(name)
      ind = random.randint(0, len(log_serv)-1)
      logging = requests.get(f"http://{services[log_serv[ind]]['Address']}:{services[log_serv[ind]]['Port']}").content

      mes_serv = []
      for name in services.keys():
         if "messages" in name:
            mes_serv.append(name)
      ind = random.randint(0, len(mes_serv)-1)
      mess = requests.get(f"http://{services[mes_serv[ind]]['Address']}:{services[mes_serv[ind]]['Port']}").content
      return str(mess)[2:-3] + ": " + str(logging)[2:-1]
       
if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8080, debug=True)