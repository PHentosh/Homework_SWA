import hazelcast
import time

print("Wating for values to be inserted")
time.sleep(60)

print("Trying to connet")
client = hazelcast.HazelcastClient(
cluster_name="logs", 
cluster_members=[
    "hazelcast-1",
    "hazelcast-2",
    "hazelcast-3"
]
)

if client is not None:
  print("Connection established")
else:
  print("Connection not established")
  exit(1)

map_t = client.get_map("test_without")
num = 0
print("Start counting")
for i in range(1000):
  val = int(map_t.get(1).result())
  time.sleep(5)
  val += 1
  num = val 
  map_t.put(1, val)
client.shutdown()
print("Without Locking: " + str(num))
