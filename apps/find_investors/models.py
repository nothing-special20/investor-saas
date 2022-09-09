from django.db import models

# Create your models here.
class Sales(models.Model):
    PIN = models.TextField()
    FOLIO = models.TextField()
    SALE_AMOUNT = models.TextField()
    SALE_DATE = models.TextField()
    GRANTOR = models.TextField()
    GRANTEE = models.TextField()
    COUNTY = models.TextField()

class ParcelInfo(models.Model):
    PIN = models.TextField()
    FOLIO = models.TextField()
    OWNER = models.TextField()
    ADDR_1 = models.TextField()
    ADDR_2 = models.TextField()
    CITY = models.TextField()
    STATE = models.TextField()
    ZIP = models.TextField()
    NUMBER_OF_BEDS = models.TextField()
    NUMBER_OF_BATHS = models.TextField()
    SQUARE_FEET = models.TextField()
    YEAR_BUILT = models.TextField()
    NUMBER_OF_STORIES = models.TextField()
    NUMBER_OF_UNITS = models.TextField()
    ACREAGEACREAGE = models.TextField()
    COUNTY = models.TextField(default=None, blank=True, null=True)

class ParcelCoordinates(models.Model):
    PIN = models.TextField()
    FOLIO = models.TextField()
    LATITUDE = models.DecimalField(max_digits=19, decimal_places=16)
    LONGITUDE = models.DecimalField(max_digits=19, decimal_places=16)
    COUNTY = models.TextField() 