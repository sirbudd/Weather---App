import pickle
import json   
from multiprocessing import shared_memory
import smtplib
import logging

#separate file for functions that are used globally

def open_cfg():
    """
    Function for opening the cfg file.
    """
    try:
        jsonfile =  open("cfg.json", "r")
        data = json.load(jsonfile)
    except IOError:
        print("Failed to read JSON Config File")
    
    try:
        city_name = data['city']
        city_name = str(city_name)
    except ValueError:
        print('City must be a string')

    return data

    
#     return data

# def open_cfg():
#     """
#     Function for opening the cfg file.
#     """
#     jsonfile =  open("cfg.json", "r")
#     data = json.load(jsonfile)
    
#     return data