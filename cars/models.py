from django.db import models
from django.contrib.auth.models import User
from brands.models import Brands


# =========================
# CAR MODEL (ENHANCED)
# =========================
class Car(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(
        upload_to='cars/media/uploads',
        blank=True,
        null=True
    )

    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    buyers = models.ManyToManyField(
        User,
        related_name='bought_cars',
        blank=True
    )

    # ⭐ Rating (future-ready)
    rating = models.FloatField(default=0)

    # =========================
    # 🔧 ADMIN-CONTROLLED SPECIFICATIONS
    # =========================
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('Petrol', 'Petrol'),
            ('Diesel', 'Diesel'),
            ('Electric', 'Electric'),
            ('CNG', 'CNG'),
        ]
    )

    transmission = models.CharField(
        max_length=20,
        choices=[
            ('Manual', 'Manual'),
            ('Automatic', 'Automatic'),
        ]
    )

    mileage = models.CharField(max_length=20)   # Example: 20 km/l
    seating = models.PositiveIntegerField()      # Example: 5

    def __str__(self):
        return self.name


# =========================
# COMMENT MODEL
# =========================
class Comment(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name}'


# =========================
# ❤️ WISHLIST MODEL
# =========================
class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE
    )
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"
    
    
# =========================
# ⭐ USER RATING MODEL
# =========================
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()  # 1 to 5
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.rating})"
