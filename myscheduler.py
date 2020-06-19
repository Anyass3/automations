from apscheduler.schedulers.blocking import BlockingScheduler
from is_connected import connect_to_wifi

sched = BlockingScheduler()

# Schedule job_function to be called every time specified
sched.add_job(connect_to_wifi, 'interval', seconds=3)

sched.start()
