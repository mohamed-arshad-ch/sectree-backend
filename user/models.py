from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=100,null=True,blank=True)
    laname = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=100,null=True,blank=True)
    porifile_img = models.ImageField()
    wallet = models.CharField(max_length=100,default="0",blank=True)
    right_parent = models.CharField(max_length=100,null=True,blank=True)
    left_parent = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    refferal_code = models.CharField(default=uuid.uuid4().hex[:5],max_length=150,blank=True)
    active = models.BooleanField(default=True)



    def __str__(self):
        return self.username