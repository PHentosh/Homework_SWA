import hazelcast

client = hazelcast.HazelcastClient(
cluster_name="inst", 
)

# Create a Distributed Map in the cluster
map_t = client.get_map("test_app").blocking() 


for i in range(1000):
  map_t.put(i, str(i))

client.shutdown()


Агенти часу +
Тусовщик кунмін +