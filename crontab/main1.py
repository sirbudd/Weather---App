#\#!/bin/env python
from crontab import CronTab

cron = CronTab(user='sirbudd')

job = cron.new(command='python /home/sirbudd/Desktop/Github/Weather---App/crontab/ex.py')
job.minute.every(1)
cron.write()

print(job.is_valid())