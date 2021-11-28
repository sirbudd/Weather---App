import pickle
import time
import requests
import json   
from multiprocessing import shared_memory
import smtplib

#TODO IMPLEMENT CRONTAB


def open_cfg():
    """
    Function for opening the cfg file.
    """
    jsonfile =  open("cfg.json", "r")
    data = json.load(jsonfile)
    
    return data


def send_email():
    config = open_cfg()

    with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
        old_weather = pickle.load(file)
    
    sender = config['sender_email_address']
    password = config['sender_password']

    receiver = config['receiver_email_address']     #account login info
    
    subject = "Weather App Warning - High Delta"                                    #email title
    body = "Attention! Temperature or Humidity delta too big! New Temp & Humidity : " ,old_weather['old_temperature'],old_weather['old_humidity']  #email subject

    # header
    message = f"""From: Weather {sender}
    To: {receiver}
    Subject: {subject}\n
    {body}
    """

    server = smtplib.SMTP("smtp.gmail.com", 587)    #connect to google SMTP
    server.starttls()

    try:
        server.login(sender,password)
        print("Logged in...")
        server.sendmail(sender, receiver, message)
        print("Email has been sent!")
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in")


def consumer():
    """
    Driver function. Deserialize our data, calculate weather deltas & send emails if necessarry
    """
    config = open_cfg()
    sh_memory = shared_memory.SharedMemory('weather-shared-memory')                 #accessing our shared memory created by the producer.

    with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
        old_weather = pickle.load(file)
    print(old_weather)

    weather = pickle.loads(bytearray(sh_memory.buf[:]))                             # buf for copying the data into a new array
    print(weather)                                                                  #print our data, dictionary format : {temperature : X ; humidity : Y}

    current_temperature = weather['temperature']                                                 
    current_humidity = weather['humidity']                                          #saving our old data in a dictinary for pickling
    current_weather = {"old_temperature" : current_temperature, "old_humidity" : current_humidity}     

    temperature_delta = current_temperature - old_weather['old_temperature']
    humidity_delta = current_humidity - old_weather['old_humidity']
    threshold = config['threshold']

    with open('old_data.pickle','wb') as file:
        pickle.dump(current_weather, file)                                          #writing our new data for delta comparison

    if temperature_delta > threshold or humidity_delta > threshold:
        send_email()
    
    sh_memory.close()
    sh_memory.unlink()


if __name__ == '__main__':
    consumer()
    #send_email()
