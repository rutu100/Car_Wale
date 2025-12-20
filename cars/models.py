from django.db import models
from django.contrib.auth.models import User
from brands.models import Brands


class FuelType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(upload_to='cars/uploads/', blank=True, null=True)

    price = models.FloatField()
    on_road_price = models.FloatField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    buyers = models.ManyToManyField(
        User, related_name='bought_cars', blank=True
    )

    rating = models.FloatField(default=0)

    # ===== NEW FIELDS =====
    model_year = models.PositiveIntegerField(null=True, blank=True)
    engine = models.CharField(max_length=50, blank=True)

    BODY_CHOICES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
    ]
    body_type = models.CharField(
        max_length=20, choices=BODY_CHOICES, blank=True
    )

    # MULTIPLE FUEL TYPES
    fuel_types = models.ManyToManyField(FuelType)

    transmission = models.CharField(
        max_length=20,
        choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')]
    )

    mileage = models.CharField(max_length=20)
    seating = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Rating(models.Model):
    car = models.ForeignKey(Car, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('car', 'user')


class Comment(models.Model):
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
