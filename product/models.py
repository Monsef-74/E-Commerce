from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    WOMEN = "Women"
    MEN = "Men"
    KIDS = "Kids"
    
class Product(models.Model):
    name = models.CharField(max_length=200,default="",blank=False)
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand = models.CharField(max_length=200,default="",blank=False)    
    category = models.CharField(max_length=50,choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name 
    
    
class Review(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=500,default="",blank=False)        
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment