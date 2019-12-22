from django.db import models
from home.models import Invoice
# Create your models here.
class Company(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=100,unique=True)
    contact = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length=500,default=" Company-address")
class Rate(models.Model):
    id = models.IntegerField
    company_id = models.IntegerField(default=1)
    site_id = models.IntegerField(default=1)
    service1 = models.CharField(max_length=100)
    service2 = models.CharField(max_length=100)
    service3 = models.CharField(max_length=100)