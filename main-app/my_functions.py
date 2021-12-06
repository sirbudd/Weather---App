import pickle
import json   
from multiprocessing import shared_memory
import smtplib
import logging


def open_cfg():
    """
    Function for opening the cfg file.
    """
    jsonfile =  open("cfg.json", "r")
    data = json.load(jsonfile)
    
    return data