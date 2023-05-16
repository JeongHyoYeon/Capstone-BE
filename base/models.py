from django.db import models
from django.utils.timezone import localdate, localtime, now

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now().strftime("%Y-%m-%d %H:%M:%S")
        self.save(update_fields=['deleted_at'])

