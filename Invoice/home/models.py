from django.db import models

# Create your models here.
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=100)
    address = models.CharField(max_length=500,default=0)
    contact = models.CharField(max_length=100)

    discount = models.CharField(max_length=300)
    total_price= models.CharField(max_length=300)
    total_units= models.CharField(max_length=300)
    date= models.DateField()

class Sales(models.Model):
    inv_id= models.IntegerField()
    site_id= models.IntegerField()
    units_load= models.IntegerField()
    no_loads = models.IntegerField()
    tot_units= models.IntegerField()
    tot_price= models.IntegerField()