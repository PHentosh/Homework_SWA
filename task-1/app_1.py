import hazelcast

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
  

map_t = client.get_map("test_app").blocking()
print("Map created, sart putting some valuse")
for i in range(1000):
  if i % 10 == 0:
    print(i)
  map_t.put(i, str(i))

print("Shutting down the connection")
client.shutdown()