from django.db import models
from django.db.models.signals import post_delete
from .utils import file_cleanup
import os

# Create your models here.
class ImageSearch(models.Model):
    image = models.ImageField(upload_to='cbir/img_search', null=True)
    contrast = models.FloatField(default=0.0)
    homo = models.FloatField(default=0.0)
    entropy = models.FloatField(default=0.0)
    hue = models.FloatField(default=0.0)
    satur = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        db_table = "image_search"



class ImageDataSet(models.Model):
    image = models.ImageField(upload_to="cbir/img", null=True)
    contrast = models.FloatField(default=0.0)
    homo = models.FloatField(default=0.0)
    entropy = models.FloatField(default=0.0)
    hue = models.FloatField(default=0.0)
    satur = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)
    similarity = models.FloatField(default=0.0)

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        db_table = "images_data"


post_delete.connect(
    file_cleanup, sender=ImageDataSet, dispatch_uid="gallery.image.file_cleanup"
)
post_delete.connect(
    file_cleanup, sender=ImageSearch, dispatch_uid="gallery.image.file_cleanup"
)