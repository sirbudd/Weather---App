import pickle
import time
import requests
import logging   
from multiprocessing import shared_memory
import warnings
from my_functions import *

warnings.filterwarnings("ignore")
logging.basicConfig(filename='logs.log', level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s') #logging file config

def get_weather(config):
    """
    Function for connecting to OpenWeather Api
    Expected input : data fetched from the OpenWeather API
    Expected output : return an dictionary containing the weather data     
    """
    api_key = config['api_key']
    root_url = config['root_url']
    city_name = config['city']
    url = f"{root_url}appid={api_key}&q={city_name}"     # Building the final url for the API call
    req = requests.get(url)     # sending a get request at the url

    data_weather = req.json()

    if data_weather['cod'] == 200: # if the information was fetched we proceed to access only the required information : temperature + humidity
        temperature = float(data_weather['main']['temp']) - 273.15
        temperature = "{:.2f}".format(temperature)
        temperature = float(temperature)
        humidity = data_weather['main']['humidity']

        return {'temperature': temperature, 'humidity': humidity} #return our data as a dictionary for easier readability
    else:
        logging.error('The weather could not be fetched. Try rerunning the app or check your cfg.json file')


def push_data(data, memory):
    """
    Function for : "pickling" (serializing) our data into bytes and pushing it to the shared memory block
    """
    data = pickle.dumps(data)
    size = len(data)
    memory.buf[:size] = data


def producer():
    """
    Driver function. Collecting oud weather data and pushing it to shared memory.
    Expected input : shared memory parameters, weather data from get_weather function
    Expected output : data serialized & pushed to shared memory
    """
    try:
        config = open_cfg()
        
        sh_memory = shared_memory.SharedMemory(create = True, size = config['sh_size'] , name = 'weather-shared-memory')   #creating out shared memory, configurable size
        data = get_weather(config)   #getting our weather info
        if not data:                 #checking if the data is valid
            return
        push_data(data, sh_memory)   #calling our function to push our data to shared memory
        time.sleep(config['time_to_sleep_seconds'])     #configurable time to keep the shared memory saved in memory in SECONDS
        logging.info("Producer shared memory closed after %d seconds\n================" % config['time_to_sleep_seconds'])
    except KeyboardInterrupt:
        sh_memory.close()
        sh_memory.unlink()
    except:
        logging.error("Check your sh_size, time_to_sleep_seconds inside cfg.json")


if __name__ == '__main__':
    producer()
