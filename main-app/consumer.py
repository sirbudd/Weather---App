import pickle
import json   
from multiprocessing import shared_memory
import smtplib
import logging
from my_functions import *

logging.basicConfig(filename='logs.log', level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s') #logging file config


def send_email():
    """
    Function that connects to a given SMTP (google, in our case) and sends an email
    """
    config = open_cfg()

    with open('old_data.pickle', 'rb') as file:   #opening the old Temp & Humidity data
        old_weather = pickle.load(file)
    
    sender = config['sender_email_address']
    password = config['sender_password']          #account login info for sender & receiver
    receiver = config['receiver_email_address']     
    
    subject = "Weather App Warning - High Delta" #email title
    body = "Attention! Temperature or Humidity delta too big! New Temp & Humidity : " ,old_weather['old_temperature'],old_weather['old_humidity']  #email text

    # header
    message = f"""From: Weather {sender}
    To: {receiver}
    Subject: {subject}\n
    {body}"""

    server = smtplib.SMTP("smtp.gmail.com", 587)    #connect to google SMTP
    server.starttls()

    try:
        server.login(sender,password)
        print("Logged in...")
        server.sendmail(sender, receiver, message)
        print("Delta too high. Email has been sent!")
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in")


# def weather_delta(current_humidity,current_temperature):
#     """
#     Function for calculating our weather delta and deciding if an email should be sent
#     """
#     config = open_cfg()

#     with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
#         old_weather = pickle.load(file)

#     temperature_delta = current_temperature - old_weather['old_temperature']
#     humidity_delta = current_humidity - old_weather['old_humidity']                 #calculatig the delta between current & old weather data
#     threshold = config['threshold']

#     if temperature_delta > threshold or humidity_delta > threshold:                 # if delta > threshold sned warning email
#         send_email()
#         logging.info("Email has been sent")    


def consumer():
    """
    Driver function. Deserialize our data, calculate weather deltas & send emails if necessarry
    """
    config = open_cfg()
    sh_memory = shared_memory.SharedMemory('weather-shared-memory')                 #accessing our shared memory created by the producer.

    with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
        old_weather = pickle.load(file)                                             #we're using it for delta comparison
    
    weather = pickle.loads(bytearray(sh_memory.buf[:]))                             #buf for copying the data into a new array

    current_temperature = weather['temperature']                                                 
    current_humidity = weather['humidity']                                          #saving our newly generated data in a dictinary for pickling
    current_weather = {"old_temperature" : current_temperature, "old_humidity" : current_humidity}     #this information becomes the old data

    logging.info(config['city'])
    logging.info(weather)               #logging the current generated weather info

    temperature_delta = current_temperature - old_weather['old_temperature']
    humidity_delta = current_humidity - old_weather['old_humidity']                 #calculatig the delta between current & old weather data
    threshold = config['threshold']
    
    with open('old_data.pickle','wb') as file:
        pickle.dump(current_weather, file)                                          #writing our new data for delta comparison
    
    if temperature_delta > threshold or humidity_delta > threshold:                 # if delta > threshold sned warning email
        send_email()
        logging.info("Email has been sent")
    
    sh_memory.close()
    sh_memory.unlink()
    logging.info("Shared memory closed\n================")


if __name__ == '__main__':
    consumer()