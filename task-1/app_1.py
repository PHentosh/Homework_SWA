import hazelcast

print("Connecting")

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



map_1 = client.get_map("test_without").blocking()
map_1.put(1, 1)
map_2 = client.get_map("test_pesimistic").blocking()
map_2.put(1, 1)
map_3 = client.get_map("test_optimistic").blocking()
map_3.put(1, 1)

print("Shutting down the connection")
client.shutdown()