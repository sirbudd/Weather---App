import pickle
from multiprocessing import shared_memory

sh_memory = shared_memory.SharedMemory('weather-shared-memory')


def consumer():
    weather = pickle.loads(bytearray(sh_memory.buf[:]))
    print(weather)


consumer()
