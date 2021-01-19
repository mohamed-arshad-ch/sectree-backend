from .views import *
from knox import views as knox_views
from django.urls import path

urlpatterns = [

    #User Module
    path('api/v1/user/register', RegisterAPI.as_view(), name='register'),
    path('api/v1/user/login/', LoginAPI.as_view(), name='login'),
    path('api/v1/user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/v1/user/search', UserListView.as_view(), name='userlist'),
    path('api/v1/user/update/<int:id>', UpdateUser.as_view(), name='updateuser'),
    path('api/v1/user/read/<int:id>', ReadUserList.as_view(), name='readuserlist'),
    path('api/v1/user/rest/request', RestRequest.as_view(), name='restrequest'),
    path('api/v1/user/rest/verify', RestVerify.as_view(), name='restverify'),
    path('api/v1/user/delete', DeleteAllUser.as_view(), name='deletealluser'),


    #Payment Module

    path('api/v1/order/create', PaymentOrderCreate.as_view(), name='paymentcreate'),
    path('api/v1/order/verify', PaymentOrderVerify.as_view(), name='paymentverify'),
    path('api/v1/order/update/<str:id>', PaymentOrderUpdate.as_view(), name='paymentorderupdate'),
    path('api/v1/order/delete/<str:id>', PaymentOrderDelete.as_view(), name='paymentorderdelete'),
    path('api/v1/order/status/<str:id>', PaymentOrderStatus.as_view(), name='paymentorderstatus'),
    path('api/v1/order/read/search', PaymentOrderSearch.as_view(), name='paymentordersearch'),

    # path('api/v1/order/read/invoice', generate_pdf, name='invoice'),




    
]