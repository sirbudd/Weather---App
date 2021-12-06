import pickle
import time
import requests
import json   
from multiprocessing import shared_memory
from my_functions import *


def get_weather(config):
    """
    Function for connecting to OpenWeather Api
    """
    
    api_key = config['api_key']
    root_url = config['root_url']
    city_name = config['city']

    print(city_name)

    url = f"{root_url}appid={api_key}&q={city_name}"     # Building the final url for the API call
    req = requests.get(url)     # sending a get request at the url

    data_weather = req.json()

    # if the information was fetched we proceed to access only the required information : temperature + humidity
    if data_weather['cod'] == 200:
        temperature = float(data_weather['main']['temp']) - 273.15
        #temperature = temperature - 273.15 # converting to Celsius
        temperature = "{:.2f}".format(temperature)
        temperature = float(temperature)
        humidity = data_weather['main']['humidity']
    
        print("Temperature : ", temperature)
        print("Humidity : ",humidity)

        return {'temperature': temperature, 'humidity': humidity} #return our data as a dictionary for easier readability
    else:
        print('The weather could not be fetched. Try rerunning the app or check your cfg.sjon file')



def push_data(data, memory):
    """
    Function for : "pickling" (serializing) our data into bytes and pushing it to the shared memory block
    """
    data = pickle.dumps(data)
    size = len(data)
    memory.buf[:size] = data
    print('pushed to shared memory')


def producer():
    """
    Driver function. Collecting oud weather data and pushing it to shared memory.

    """
    try:
        config = open_cfg()
        
        sh_memory = shared_memory.SharedMemory(create = True, size = config['sh_size'] , name = 'weather-shared-memory')   #creating out shared memory, configurable size
        
        data = get_weather(config)   #getting our weather info
        if not data:                 #checking if the data is valid
            return
        push_data(data, sh_memory)   #calling our function to push our data to shared memory
        time.sleep(config['time_to_sleep_seconds'])     #configurable time to keep the shared memory saved in memory in SECONDS
        print("Producer shared memory closed after %d seconds" % config['time_to_sleep_seconds'])
    except KeyboardInterrupt:
        sh_memory.close()
        sh_memory.unlink()


if __name__ == '__main__':
    producer()
