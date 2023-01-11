from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(default='1.jpg', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name) 

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('outdoor','outdoor')
    )

    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Pending','Pending'),
    )

    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    

