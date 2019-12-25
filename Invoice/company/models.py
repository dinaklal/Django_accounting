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
class DelNote(models.Model):
    id = models.IntegerField
    del_note_id = models.IntegerField(default=1)
    company_id = models.IntegerField(default=1)
    site_id = models.IntegerField(default=1)
    service = models.CharField(max_length=100)
    date = models.DateField()
    units = models.CharField(max_length=300)
    veh_no = models.CharField(max_length=300)
    invoiced = models.BooleanField(default = False) 
    inv_id = models.IntegerField(default=0)
