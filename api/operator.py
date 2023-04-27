from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from api.auto_functions import DeletePhotos


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    delete_photos = DeletePhotos()
    scheduler.add_job(delete_photos.s3_delete, CronTrigger.from_crontab('0 0 * * *'))
    scheduler.add_job(delete_photos.db_delete, CronTrigger.from_crontab('0 0 * * *'))
    scheduler.start()

