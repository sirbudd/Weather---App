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

    sender = config['weather.app.test.python@gmail.com']
    password = config['sender_password']

    receiver = config['receiver_email_address'] #account login info
    
    subject = "Python email test" #email title
    body = "Attention! Temperature or Humidity delta too big! New Temp & Humidity : "  #email subject

    # header
    message = f"""From: Weather {sender}
    To: {receiver}
    Subject: {subject}\n
    {body}
    """

    server = smtplib.SMTP("smtp.gmail.com", 587) #connect to google SMTP
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
    """
    sh_memory = shared_memory.SharedMemory('weather-shared-memory')
    weather = pickle.loads(bytearray(sh_memory.buf[:]))
    print(weather)
    sh_memory.close()
    sh_memory.unlink()


if __name__ == '__main__':
    consumer()
    send_email()
