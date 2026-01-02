from django.urls import path
from . import views

urlpatterns = [

    # 🏠 HOME
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),


    # 🔍 LIVE SEARCH SUGGESTIONS (AJAX)
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    # 🚗 CAR CRUD
    path('add_cars/', views.add_cars, name='add_cars'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    
    
    path('compare/', views.compare_cars, name='compare_cars'),


    # ❤️ WISHLIST
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('rate/<int:car_id>/', views.rate_car, name='rate_car'),
    
    path('test-drive/', views.test_drive, name='test_drive'),
    path('my-test-drives/', views.my_test_drives, name='my_test_drives'),
    path('cancel-test-drive/<int:drive_id>/', views.cancel_test_drive, name='cancel_test_drive'),




]
