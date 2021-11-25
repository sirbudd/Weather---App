import pickle
from multiprocessing import shared_memory

sh_memory = shared_memory.SharedMemory('weather-shared-memory')

data = []

for x in range(1000):
    data.append(sh_memory.buf[x])

weather = pickle.loads(bytearray(data))

print(weather)
