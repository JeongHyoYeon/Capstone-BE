from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from api.auto_functions import s3_delete, db_delete

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(s3_delete, CronTrigger.from_crontab('0 0 * * *'))
    scheduler.add_job(db_delete, CronTrigger.from_crontab('0 0 * * *'))
    scheduler.start()

