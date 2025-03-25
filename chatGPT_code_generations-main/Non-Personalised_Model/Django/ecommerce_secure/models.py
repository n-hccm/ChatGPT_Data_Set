# ecommerce/models.py
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_points = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_points = models.IntegerField(default=0)

    def calculate_total(self):
        self.total_points = sum(product.price_points for product in self.products.all())
        self.save()


class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=1000)  # Give new users 1000 points

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
