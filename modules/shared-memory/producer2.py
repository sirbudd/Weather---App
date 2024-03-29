import pickle
import time
import requests
import json   
from multiprocessing import shared_memory

#TODO IMPLEMENT CRONTAB


def open_cfg():
    """
    Function for opening the cfg file.
    """
    jsonfile =  open("cfg.json", "r")
    data = json.load(jsonfile)
    
    return data


def get_weather(config):
    """
    Function for connecting to OpenWeather Api

    """
    config = open_cfg()
    api_key = config['api_key']
    root_url = config['root_url']
    city_name = config['city']

    print("Chosen city: " + city_name) #for testing purposes 
    
    # Building the final url for the API call
    url = f"{root_url}appid={api_key}&q={city_name}"
    # sending a get request at the url
    req = requests.get(url)

    # checking wether the information was fetched
    if not req.status_code == 200:
        print('The weather could not be fetched')
        return

    #print(req.json()) # --> print all the info fetched from the api

    data_weather = req.json()

    # if the information was fetched we proceed to access only the required information : temperature + humidity
    if data_weather['cod'] == 200:
        temperature = float(data_weather['main']['temp'])
        temperature = temperature - 273.15 # converting to Celsius
    
        humidity = data_weather['main']['humidity']
    
        print("Temperature : {:0.2f}ºC.".format(temperature))
        print("Humidity : ",humidity)

        return {'temperature': temperature, 'humidity': humidity} #return our data as a dictionary for easier readability


def push_data(data, memory):
    """
    Function for : "pickling" (serializing) our data into bytes and pushing it to the shared memory block
    """
    data = pickle.dumps(data)
    size = len(data)
    memory.buf[:size] = data
    print('pushed to shared memory')


def producer():
    try:
        config = open_cfg()
        #print(config)
        sh_memory = shared_memory.SharedMemory(create = True, size = config['sh_size'] , name = 'weather-shared-memory')
        data = get_weather(config)
        if not data:
            return
        push_data(data, sh_memory)
        time.sleep(config['time_to_sleep'])
    except KeyboardInterrupt:
        sh_memory.close()
        sh_memory.unlink()

if __name__ == '__main__':
    producer()
