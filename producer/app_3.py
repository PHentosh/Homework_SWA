import hazelcast
import time

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

for i in range(1000):
    print(f"Trying to put {i}")
    MyQueue.put(i)
    print(f"Put {i}, {MyQueue.remaining_capacity()} space left")
    time.sleep(3)

client.shutdown()