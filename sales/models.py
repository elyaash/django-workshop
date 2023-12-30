from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self) -> str:
        return self.description
    
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']



class Csv(models.Model):
    STATUS_CHOICE_DEFAULT = 'P'
    STATUS_CHOICE = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    filename = models.FileField(upload_to='csvs')
    upload_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICE, default=STATUS_CHOICE_DEFAULT)


    

    def __str__(self) -> str:
        return self.filename.name
    
# Create your models here.
class Sales(models.Model):

    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    salesmen    = models.ForeignKey(User,on_delete=models.CASCADE)
    qty   = models.IntegerField(default =1)
    sales_date  =  models.DateField(auto_now_add = True)  
    
    class Meta:
        verbose_name = "sales"
        verbose_name_plural = "sales"

    def __str__(self) -> str:
        return "{}".format(self.qty)