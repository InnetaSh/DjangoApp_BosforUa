from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_trip/', views.create_trip_view, name='create_trip'),
    path('api/get-stations/', views.get_stations, name='get_stations'),
    path('search_tickets/', views.search_tickets, name='search_tickets')
]
