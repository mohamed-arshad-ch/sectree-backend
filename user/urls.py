from .views import *
from knox import views as knox_views
from django.urls import path

urlpatterns = [
    path('api/v1/user/register', RegisterAPI.as_view(), name='register'),
    path('api/v1/user/login/', LoginAPI.as_view(), name='login'),
    path('api/v1/user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/v1/user/search', UserListView.as_view(), name='userlist'),
    path('api/v1/user/update/<int:id>', UpdateUser.as_view(), name='updateuser'),


    
]