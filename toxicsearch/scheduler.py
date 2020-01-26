import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import add_movies_to_database, add_series_to_database
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", days=7, replace_existing=True)
def update_database():
    time.sleep(random.randrange(1, 100, 1)/100.)
    add_movies_to_database()
    add_series_to_database()
    # raise ValueError("Olala!")


register_events(scheduler)

scheduler.start()
