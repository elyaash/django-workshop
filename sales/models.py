from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    qty = models.IntegerField()
    image = models.ImageField()

class Csv(models.Model):
    STATUS_CHOICE_DEFAULT = 'P'
    STATUS_CHOICE = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    filename = models.FileField()
    upload_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=5, choices = STATUS_CHOICE, default=STATUS_CHOICE_DEFAULT)

# Create your models here.
class Sales(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    salesmen    = models.ForeignKey(User,on_delete=models.CASCADE)
    qty   = models.IntegerField(default =1)
    sales_date  =  models.DateField(auto_now_add = True)  
    
