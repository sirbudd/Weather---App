import pickle
import time
import requests
import json   

from multiprocessing import shared_memory



def get_weather():
    api_key = "1802c892bb5f02f5ed354ddd4ee2ba89"
    root_url = "http://api.openweathermap.org/data/2.5/weather?"

    # City name for which we need the weather data
    with open("cfg.json", "r") as jsonfile:
        data = json.load(jsonfile)                 #opening json.config where the city's name is stored
        city_name = data['city']
        print(city_name) #for testing purposes 
    
    # Building the final url for the API call
    url = f"{root_url}appid={api_key}&q={city_name}"
    # sending a get request at the url
    req = requests.get(url)

    if not req.status_code == 200:
        print('The weather could not be fetched')
        return
    print(req.json()) #print all the info

    data_weather = req.json()

    if data_weather['cod'] == 200:
        temperature = float(data_weather['main']['temp'])
        temperature = temperature - 273.15 # converting to celsius
    
        humidity = data_weather['main']['humidity']
    
        print("Temperature : {:0.2f}ºC.".format(temperature))
        print("Humidity : ",humidity)

        return {'temperature': temperature, 'humidity': humidity}


def push_data(data, memory):
    data = pickle.dumps(data)
    size = len(data)
    memory.buf[:size] = data
    print('pushed to shared memory')


def producer():
    try:
        sh_memory = shared_memory.SharedMemory(create=True, size=1000, name='weather-shared-memory')
        data = get_weather()
        if not data:
            return
        push_data(data, sh_memory)
        # push to shared memory
        time.sleep(15)
    except KeyboardInterrupt:
        sh_memory.close()
        sh_memory.unlink()

if __name__ == '__main__':
    producer()
