import pickle
from multiprocessing import shared_memory
import smtplib
import logging
import warnings
from my_functions import *

warnings.filterwarnings("ignore")
logging.basicConfig(filename='logs.log', level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s') #logging file config

config = open_cfg()  #open our config file

def send_email():
    """
    Function that connects to a given SMTP (google, in our case) and sends an email
    Expected input : data from old_data.pickle
    Expected output : succesfull email sent
    """
    try:
        with open('old_data.pickle', 'rb') as file:   #opening the old Temp & Humidity data
            old_weather = pickle.load(file)
    except:
        logging.error("Pickled data couldn't be deserialized")

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
        server.sendmail(sender, receiver, message)
    except smtplib.SMTPAuthenticationError:
        logging.error("Unable to sign in, check your credentials")


def consumer():
    """
    Driver function. Deserialize our data, calculate weather deltas & send emails if necessarry
    Expected input : weather data from shared memory produced by producer.py
    Expected output : inside logs.log : city name, weather info, state of email, state of memory
    """
    sh_memory = shared_memory.SharedMemory('weather-shared-memory')                 #accessing our shared memory created by the producer.
    
    try:
        with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
            old_weather = pickle.load(file)                                             #we're using it for delta comparison
        weather = pickle.loads(bytearray(sh_memory.buf[:]))                             #buf for copying the data into a new array
    except:
        logging.error("Pickled data couldn't be deserialized")    
    
    current_temperature = weather['temperature']                                                 
    current_humidity = weather['humidity']                                          #saving our newly generated data in a dictinary for pickling
    current_weather = {"old_temperature" : current_temperature, "old_humidity" : current_humidity}     #this information becomes the old data

    logging.info(config['city'])
    logging.info(weather)               #logging the current generated weather info

    temperature_delta = current_temperature - old_weather['old_temperature']
    humidity_delta = current_humidity - old_weather['old_humidity']                 #calculatig the delta between current & old weather data
    threshold_temperature = config['threshold_temperature']
    threshold_humidity = config['threshold_humidity']
    
    with open('old_data.pickle','wb') as file:
        pickle.dump(current_weather, file)                                          #writing our new data for delta comparison
    
    try:
        if temperature_delta > threshold_temperature:                 # if delta > threshold send warning email
            send_email()
            logging.info("Email has been sent")
        elif humidity_delta > threshold_humidity:
            send_email()
            logging.info("Email has been sent")
    except ValueError:
        logging.error("Check your .cfg threshold values")
    
    sh_memory.close()
    sh_memory.unlink()
    logging.info("Shared memory closed")


if __name__ == '__main__':
    consumer()