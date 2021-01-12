from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.response import Response

from .models import *
import uuid
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    refferalcode = serializers.CharField(default="")
    class Meta:
        
        model = CustomUser
        fields = ('fname' ,'laname','phone_number','porifile_img','username', 'email', 'password','refferalcode')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        if len(validated_data['refferalcode']) == 0:
            user = CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'],fname=validated_data['fname'],laname=validated_data['laname'],phone_number=validated_data['phone_number'],porifile_img=validated_data['porifile_img'])

            return user,2
        else:
            print("in")
            try:
                refuser = CustomUser.objects.get(refferal_code=validated_data['refferalcode'])
                
                if refuser.left_parent:
                    print("left alredy done")
                    if refuser.right_parent:
                        print("right already done")
                    else:
                        user = CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'],fname=validated_data['fname'],laname=validated_data['laname'],phone_number=validated_data['phone_number'],porifile_img=validated_data['porifile_img'])

                
                        refuser.right_parent = user.username
                        refuser.wallet = int(refuser.wallet) + int(user.wallet)
                        refuser.save()
                else:
                    user = CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'],fname=validated_data['fname'],laname=validated_data['laname'],phone_number=validated_data['phone_number'],porifile_img=validated_data['porifile_img'])

                
                    refuser.left_parent = user.username
                    refuser.wallet = int(refuser.wallet) + int(user.wallet)
                    refuser.save()
                return user,2
            except CustomUser.DoesNotExist:
                print("not exist")
                # newuser = CustomUser.objects.get(username="admin")
                # return newuser
                return {"message":"inavlid Token"},1

        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','fname','laname','phone_number','porifile_img','wallet','right_parent','left_parent', 'username', 'email','password')
        extra_kwargs = {'password': {'write_only': True}}


class SendOtpSerializer(serializers.ModelSerializer):
    emailaddress = serializers.EmailField(default="")
    class Meta:
        model = CustomUser
        fields = ('id','emailaddress')
