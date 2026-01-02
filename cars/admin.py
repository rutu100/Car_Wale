from django.contrib import admin
from .models import Car, FuelType, Wishlist, Comment, Rating,TestDrive



# =========================
# CAR ADMIN
# =========================
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    # Show these columns in admin list
    list_display = (
        'name',
        'brand',
        'price',
        'on_road_price',
        'quantity',
        'model_year',
        'transmission',
        'fuel_list',
        'rating',
    )

    # Filters on right side
    list_filter = (
        'brand',
        'body_type',
        'transmission',
        'model_year',
    )

    # Search box
    search_fields = (
        'name',
        'brand__name',
        'engine',
    )

    # ManyToMany field display helper
    def fuel_list(self, obj):
        return ", ".join(f.name for f in obj.fuel_types.all())

    fuel_list.short_description = "Fuel Types"


# =========================
# FUEL TYPE ADMIN
# =========================
@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# =========================
# RATING ADMIN
# =========================
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('car__name', 'user__username')


# =========================
# COMMENT ADMIN
# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('car', 'name', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('car__name', 'name', 'email')


# =========================
# WISHLIST ADMIN
# =========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'added_on')
    search_fields = ('user__username', 'car__name')
  

@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'car',
        'preferred_date',
        'preferred_slot',
        'status',
        'created_at'
    )
    list_filter = ('status', 'preferred_date')
    search_fields = ('name', 'phone', 'car__name')
