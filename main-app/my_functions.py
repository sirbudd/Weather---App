import json   
from multiprocessing import shared_memory

#separate file for functions that are used globally

def open_cfg():
    """
    Function for opening the cfg file.
    Expected input : correct parameters from the cfg.json file
    Expected outpt : data loaded into data variable
    """
    try:
        jsonfile =  open("cfg.json", "r")
        data = json.load(jsonfile)
    except IOError:
        print("Failed to read JSON Config File")    
    return data
