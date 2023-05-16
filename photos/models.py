from django.db import models
from accounts.models import User
from trips.models import Trip
from base.models import BaseModel


class Photo(BaseModel):
    file_key = models.UUIDField(unique=True)
    file_name = models.CharField(blank=True, max_length=255)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    url = models.TextField()
    tag_yolo = models.ManyToManyField('TagYolo', related_name='photos')
    tag_face = models.ManyToManyField('TagFace', related_name='photos')
    taken_at = models.DateTimeField(null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_sorted_yolo = models.BooleanField(default=False)


class TagYolo(models.Model):
    tag_name = models.CharField(max_length=20)
    tag_name_kr = models.CharField(max_length=20)


class TagFace(models.Model):
    tag_num = models.IntegerField()
    custom_name = models.CharField(blank=True, max_length=255)


