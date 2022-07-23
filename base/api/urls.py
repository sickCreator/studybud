from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoute),
    path('rooms/', views.getRooms),
    path('rooms/<str:room_id>/', views.getRoom)
]
