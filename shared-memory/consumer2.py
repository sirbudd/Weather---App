import pickle
from multiprocessing import shared_memory



def consumer():
    sh_memory = shared_memory.SharedMemory('weather-shared-memory')
    weather = pickle.loads(bytearray(sh_memory.buf[:]))
    print(weather)
    sh_memory.close()
    sh_memory.unlink()


if __name__ == '__main__':
    consumer()
