from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, RegisterSerializer, UserUpdateSerializer
from django.contrib.auth import login
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import *
import boto3

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    pagination_class.page_size_query_param = 'limit'
    search_fields = ['username']

class UpdateUser(generics.UpdateAPIView):
    
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request,id):
        queryset = CustomUser.objects.get(id=id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def update(self, request,id,*args):
        
        queryset = CustomUser.objects.get(id=id)
        
        queryset.username = request.data.get("username")
        queryset.email = request.data.get("email")
        queryset.set_password(request.data.get("password"))
        queryset.fname = request.data.get("fname")
        queryset.laname = request.data.get("laname")
        queryset.phone_number = request.data.get("phone_number")
        queryset.porifile_img = request.data.get("porifile_img")
        queryset.wallet = request.data.get("wallet")
        queryset.right_parent = request.data.get("right_parent")
        queryset.left_parent = request.data.get("left_parent")
        




        queryset.save()

        serializer = self.get_serializer(queryset)
        

        return Response(serializer.data)
    

class ReadUserList(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = CustomUser.objects.get(id=id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class RestRequest(generics.GenericAPIView):
    
    def get(self, request):
        # Create an SNS client
        client = boto3.client(
            "sns",
            aws_access_key_id="AKIAJZCVGDCSNMEKDVBA",
            aws_secret_access_key="q1dm33uqbLPPZ17RZoNQ1QxmdVh/ln4EKpDrQWFT",
            region_name="ap-south-1"
        )

        
        # Send your sms message.
        responce = client.publish(
            
            PhoneNumber="+919847274569",
            Message="Hello World!"
        )

        
        return Response(data=responce)

class DeleteAllUser(generics.GenericAPIView):

    serializer_class = UserSerializer

    def delete(self,request):

        queryset = CustomUser.objects.all().delete()
        
        return Response({"message":"Dlete All User Successfully"})