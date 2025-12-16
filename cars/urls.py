from django.urls import path
from . import views

urlpatterns = [
    path('add_cars/', views.add_cars, name='add_cars'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),

    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
]
