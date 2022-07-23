from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    # pk is a primary key or id will be an integer

    path('room/<str:pk>', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create_room/', views.createRoom, name='create_room'),
    path('update_room/<str:pk>/', views.updateRoom, name='update_room'),
    path('delete_room/<str:pk>/', views.deleteRoom, name='delete_room'),
    path('delete_message/<str:pk>/', views.deleteMessage, name='delete_message'),
    path('update_user/', views.updateUser, name='update_user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activities, name='activity')

]
