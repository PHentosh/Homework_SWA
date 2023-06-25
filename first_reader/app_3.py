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

MyQueue = client.get_queue("queue").blocking()

while True:
    i = MyQueue.take()
    print(f"Just get {i}")

client.shutdown()