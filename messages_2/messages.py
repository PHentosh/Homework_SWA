from flask import Flask, request
import hazelcast
import threading
import os



messages = []

def listener():
    global messages

    client = hazelcast.HazelcastClient(
    cluster_name="logs", 
    cluster_members=["hazelcast-queue"
    ])

    queue = client.get_queue("MQ").blocking()
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