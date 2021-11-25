import pickle
from multiprocessing import shared_memory

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BlockingScheduler()
sh_memory = shared_memory.SharedMemory(create=True, size=1000, name='weather-shared-memory')

@scheduler.scheduled_job(
    CronTrigger(year='*', month='*', day='*', week='*', day_of_week='*', hour='0', minute=0, second=0)
)
def train_model():
    pass
    # Implement producer
    # fetch data from api



    # push to shared memory
    data = {'weather': '30degrees', 'humidity': 50}
    index = 0

    # poate gasim o metoda mai buna
    for b in pickle.dumps(data):
        sh_memory.buf[index] = b
        index += 1

try:
    scheduler.start()
except KeyboardInterrupt:
    sh_memory.close()
    sh_memory.unlink()

print('Nu ajunge aici')
