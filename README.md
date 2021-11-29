# Weather---App
Weather App - Project

## Libriaries/Frameworks used

1. [Pickle](https://docs.python.org/3/library/pickle.html)
    - `pip install pickle`
2. [Crontab](https://pypi.org/project/python-crontab/)
    - `pip install python-crontab`

In the early stages the app was built using "modules" which can be found in the Modules folder

## Configuring you parameters

### The app is in main-app

First open `cfg.json` and edit it for your needs.

The `"city"` parameter is for configuring your city.

The `"sender_email_address"` , `"sender_password"` ,`"root_url"`, `"api_key"` can be left as is.

The `"time_to_sleep"` parameter is for configuring how many seconds you want your shared memory block to remain assigned.

The `"sh_size"` parameter is for configuring your shared memory size in bytes.

The `"threshold"` parameter is for configuring your delta threshold for temperature & humidity.

The `"cron_time_minutes_producer"` and `"cron_time_minutes_consumer"` parameter is for configuring your producer/consumer repat time for your cronjobs in minutes.

The `"linux_user"` parameter is for configuring your linux user for crontab jobs, you can use `whoami` to find your user name.

## Running the app

### The app is in main-app

Run `python3 producer.py` then `python3 consumer.py`. 

The producer will connect to the Weather API (Open Weather) and store your data in a shared memory block.

The consumer will read this data, log it inside `logs.log`, send an email if the delta is too high, and close the shared memory block.

## Adding cronjobs

If you want to add those 2 python scripts to your crontab run `cronjob.py`.

Run `crontab -l` in your terminal to check if they have been added.

Run `crontab -r` to remove all cronjobs from your crontab