import pickle
import time

from multiprocessing import shared_memory

sh_memory = shared_memory.SharedMemory(create=True, size=1000, name='weather-shared-memory')


def producer():
    pass
    # Implement producer
    # fetch data from api

    # push to shared memory
    data = {'weather': '30degrees', 'humidity': 50}
    data = pickle.dumps(data)
    size = len(data)
    sh_memory.buf[:size] = data
    print('pushed to shared memory')


producer()
time.sleep(15)
sh_memory.close()
sh_memory.unlink()
