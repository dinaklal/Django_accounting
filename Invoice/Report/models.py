from django.db import models

# Create your models here.

class Account(models.Model):
    from_company= models.IntegerField()
    amount= models.CharField(max_length=300)
    date= models.DateField()
    