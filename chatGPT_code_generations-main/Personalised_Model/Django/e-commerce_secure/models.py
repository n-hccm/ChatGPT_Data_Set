from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_in_points = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost_in_points = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost_in_points = self.product.price_in_points * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
