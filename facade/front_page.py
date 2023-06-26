from flask import Flask, request
import requests
import uuid
import random
import hazelcast



app = Flask(__name__)

logging_servises = ["http://logging-1:8081",
                    'http://logging-2:8084',
                    'http://logging-3:8085'
                    ]

messages_servises = ["http://messages-1:8082",
                    'http://messages-2:8083'
                    ]

client = hazelcast.HazelcastClient(
cluster_name="logs", 
cluster_members=["hazelcast-queue"
])

queue = client.get_queue("MQ").blocking()

@app.route('/',methods = ['GET', 'POST'])
def login():
    global logging_servises
    global messages_servises
    global queue
    if request.method == 'POST':
      dat = str(request.data)[2:-1]
      u = str(uuid.uuid4().hex)
      log_json = {u:dat}
      ind = random.randint(0, 2)
      logging = requests.post(logging_servises[ind], data=str(log_json)).content
      queue.put(dat)
      return logging
    else:
      ind = random.randint(0, 2)
      logging = requests.get(logging_servises[ind]).content
      ind = random.randint(0, 1)
      mess = requests.get(messages_servises[ind]).content
      return str(mess)[2:-3] + ": " + str(logging)[2:-1]
       
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)