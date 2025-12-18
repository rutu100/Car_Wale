from django.contrib import admin
from .models import Car, Comment, Wishlist, Rating

# =========================
# CAR ADMIN
# =========================
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'price',
        'quantity',
        'fuel_type',
        'transmission',
        'mileage',
        'seating'
    )

    list_filter = (
        'brand',
        'fuel_type',
        'transmission'
    )

    search_fields = (
        'name',
        'brand__name'
    )


# =========================
# COMMENT ADMIN
# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'created_on')
    search_fields = ('name', 'car__name')


# =========================
# WISHLIST ADMIN
# =========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'added_on')

# =========================
# RATING ADMIN

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rating', 'created_on')
    list_filter = ('rating', 'created_on')






