from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    COMPUTER = 'computer', 'Computer'
    KIDS = 'kids', 'Kids'
    FOOD = 'food', 'Food'
    HOME = 'home', 'Home'

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    brand = models.CharField(max_length=100, blank=False)  # Adjusted max_length for typical brand names
    category = models.CharField(max_length=20, choices=Category.choices)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Renamed to snake_case
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ratings = models.FloatField(default=0)
    comment = models.TextField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Renamed to snake_case


    def __str__(self):
        return self.comment
