#this is to be programmed to run at start-up
#will check for wifi login every 3 secs
# if not logged in it will open the the browser and
#  drive itself to log me back in close the browser imediately
# see is_connected.py
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from is_connected import connect_to_wifi

load_dotenv()

sched = BlockingScheduler()

# Schedule job_function to be called every time specified
sched.add_job(connect_to_wifi, 'interval', seconds=3)

sched.start()
