from django.db import models
from django.utils.timezone import localdate, localtime
from accounts.models import BaseModel, Group


# Create your models here.
class Trip(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    departing_date = models.DateField(default=localdate)
    arriving_date = models.DateField(default=localdate)
    thumbnail = models.TextField(null=True)
