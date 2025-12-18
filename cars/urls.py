from django.urls import path
from . import views

urlpatterns = [

    # 🏠 HOME
    path('', views.home, name='home'),

    # 🔍 LIVE SEARCH SUGGESTIONS (AJAX)
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    # 🚗 CAR CRUD
    path('add_cars/', views.add_cars, name='add_cars'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),

    # ❤️ WISHLIST
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('rate/<int:car_id>/', views.rate_car, name='rate_car'),

]
