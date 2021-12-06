#\#!/bin/env python
import json   
from crontab import CronTab
import os
from my_functions import *

#Run this script to add consumer.py & producer.py to your crontab list

config = open_cfg()

cron = CronTab(user=os.getlogin()) #your linux user

job1 = cron.new(command='python consumer.py')  #add new job for consumer.py
job2 = cron.new(command='python producer.py')  #add new job for producer.py

job1.minute.every(config['cron_time_minutes_producer'])       #set cronjob time to repeat after in minutes
job2.minute.every(config['cron_time_minutes_consumer'])
cron.write()

print(job1.is_valid())  #check if jobs are valid
print(job2.is_valid())