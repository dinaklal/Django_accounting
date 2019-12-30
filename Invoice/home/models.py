from django.db import models

# Create your models here.
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.IntegerField()
    discount = models.CharField(max_length=300)
    amount= models.CharField(max_length=300)
    date= models.DateField()

class Invoice_Details(models.Model):
    inv_id= models.IntegerField()
    del_note_id= models.IntegerField()
    rate_id = models.IntegerField()
    