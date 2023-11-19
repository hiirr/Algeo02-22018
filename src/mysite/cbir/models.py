from django.db import models
from django.db.models.signals import post_delete
from .utils import file_cleanup
import os

# Create your models here.
class ImageSearch(models.Model):
    image = models.ImageField(upload_to='image_search', null=True)

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        db_table = "image_search"



class ImageDataSet(models.Model):
    image = models.ImageField(upload_to="image_data", null=True)
    similarity = models.FloatField(default=0.0)

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        db_table = "image_data"