import pickle #using pickle for de-serializing the data stored in shared memory
from multiprocessing import shared_memory

sh_memory = shared_memory.SharedMemory('weather-shared-memory') #accessing our shared memory produced by the producer-client

data = [] #storing our

for x in range(1000):
    data.append(sh_memory.buf[x]) #append all our data inside a list 

weather = pickle.loads(bytearray(data)) #de-serialize our data 

print(weather)
