import hazelcast, time, threading

# class Value:

#   amount = -1

#   def __init__(self, value = -1):
#     self.amount = value

#   def __eq__(self, __value: object) -> bool:
#     if __value == self:
#       return True
#     if not isinstance(__value, Value):
#       return False
#     return __value.amount == self.amount

res = [None, None, None]

def func1(future):
  global res
  res[0] = future.result()

def func2(future):
  global res
  res[1] = future.result()

def func3(future):
  global res
  res[2] = future.result()

def thread1():


  client = hazelcast.HazelcastClient(
  cluster_name="inst", 
  )

  # Create a Distributed Map in the cluster
  map_t = client.get_map("test_app")
  num = 0
  for i in range(1000):
    if i % 100 == 0: print( "Without Locking At: " + str(i) + ", num: " + str(num) )
    val = map_t.get(i).result()
    #print(val)
    time.sleep(5)
    if str(val) == str(i):
      num += 1
  client.shutdown()
  print("Without Locking: " + str(num))
  return num

def thread2():

  client = hazelcast.HazelcastClient(
  cluster_name="inst", 
  )

  # Create a Distributed Map in the cluster
  map_t = client.get_map("test_app")
  num = 0
  for i in range(1000):
    if i % 100 == 0: print( "Pessimistic Locking At: " + str(i) + ", num: " + str(num) )
    map_t.lock(i)
    try:
      val = map_t.get(i).result()
      time.sleep(5)
      if str(val) == str(i):
        num += 1

    finally:
      map_t.unlock(i)

    
  client.shutdown()
  print("Pessimistic Locking: " + str(num))
  return num

def thread3():

  client = hazelcast.HazelcastClient(
  cluster_name="inst", 
  )

  # Create a Distributed Map in the cluster
  map_t = client.get_map("test_app")
  num = 0
  for i in range(1000):
    if i % 100 == 0: print( "Optimistic Locking At: " + str(i) + ", num: " + str(num) )
    while 1:
      val = map_t.get(i).result()
      time.sleep(5)
      if str(val) == str(i):
        num += 1
        break
  client.shutdown()
  print("Optimistic Locking: " + str(num))
  return num

# client = hazelcast.HazelcastClient(
# cluster_name="inst", 
# )

# Create a Distributed Map in the cluster
# map_t = client.get_map("test_lock")
# map_t.put(1, Value())

#client.shutdown()

t1 = threading.Thread(target=thread1, args=())
t2 = threading.Thread(target=thread2, args=())
t3 = threading.Thread(target=thread3, args=())

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()