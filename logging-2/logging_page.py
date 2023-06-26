from flask import Flask, request
import hazelcast
import requests
import json


app = Flask(__name__)

client = hazelcast.HazelcastClient(
cluster_name="logs", 
cluster_members=["hazelcast-2"
])

map_t = client.get_map("logging_map").blocking()

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