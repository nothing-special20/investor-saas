from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class MyProperties(models.Model):
    PIN = models.TextField()
    TITLE = models.TextField()
    PROPERTY_DETAILS = models.TextField()
    PROPERTY_PHOTOS = ArrayField(models.ImageField(upload_to='property_photos'), size=12)
