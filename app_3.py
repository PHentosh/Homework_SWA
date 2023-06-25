import hazelcast

client = hazelcast.HazelcastClient(
cluster_name="inst", 
)
# Create a Distributed Map in the cluster
MyQueue = client.get_queue("queue").blocking()

for i in range(500):
    # MyQueue.put(i)
    # print(f"Just put {i}")
    ii = MyQueue.take()
    print(f"Just get {ii}")    

# while not MyQueue.is_empty():
#     ii = MyQueue.take()
#     print(f"Just get {ii}")

client.shutdown()