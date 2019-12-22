from django.db import models
from home.models import Invoice
# Create your models here.
class Sites(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=100,unique=True)
    Description = models.CharField(max_length=500,default="Site")
