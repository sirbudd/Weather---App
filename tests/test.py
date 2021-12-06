
def weather_delta(current_humidity,current_temperature):
    """
    Function for calculating our weather delta and deciding if an email should be sent
    """
    config = open_cfg()

    with open('old_data.pickle', 'rb') as file:                                     #opening the old Temp & Humidity data
        old_weather = pickle.load(file)

    temperature_delta = current_temperature - old_weather['old_temperature']
    humidity_delta = current_humidity - old_weather['old_humidity']                 #calculatig the delta between current & old weather data
    threshold = config['threshold']

    if temperature_delta > threshold or humidity_delta > threshold:                 # if delta > threshold sned warning email
        send_email()
        logging.info("Email has been sent")    