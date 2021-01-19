from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, RegisterSerializer, UserUpdateSerializer, SendOtpSerializer,VerifyOtpSerializer, CreatePaymentOrder , VerifyPaymentOrder,UpdatePaymentOrder
from django.contrib.auth import login
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import *
import boto3
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import send_mail
import uuid
import socket
from django.template.loader import render_to_string
import razorpay
import requests

#Start User Module
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, resid = serializer.save()
        print(resid)
        if resid == 2:
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })
        else:

            return Response(user)
    
        

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
    serializer_class = SendOtpSerializer
    def post(self, request):
        email = request.data['emailaddress']

        try:
            HOSTNAME = request.META['HTTP_HOST']
            otps = uuid.uuid4().hex[:6]
            user = CustomUser.objects.get(email=email)
            user.otp_code = otps
            user.save()
            email_url = 'http://'+str(HOSTNAME)+'/api/v1/user/rest/verify?email='+email
            email_msg = "<p>verification Code Is </p><br><h1>"+ otps +"</h1><a href='"+email_url+"'><button>Verify</button></a>"
            print(email_msg)
            email_res = send_mail('Otp Verification', 'The Otp is  '+otps, 'mohamedarshadcholasseri5050@gmail.com',[email], fail_silently=False,html_message=email_msg)

            return Response(data="Email Send Success")
        except CustomUser.DoesNotExist:

        
            return Response(data="This Email Not Logined")


class RestVerify(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer
    def post(self, request):
        
        code = request.data['verificationcode']

        try:
            user = CustomUser.objects.get(otp_code=code,email=request.GET.get('email', ''))
            user.otp_code = uuid.uuid4().hex[:6]
            user.save()
            return Response(data="Successfully Reset")

        except CustomUser.DoesNotExist:
            return Response(data="Invalid Otp Please Try Again")


class DeleteAllUser(generics.GenericAPIView):

    serializer_class = UserSerializer

    def delete(self,request):

        queryset = CustomUser.objects.all().delete()
        
        return Response({"message":"Dlete All User Successfully"})


#End User Module

#Start User Module

class PaymentOrderCreate(generics.GenericAPIView):

    serializer_class = CreatePaymentOrder
    def post(self, request):
        

        

        
        
        client = razorpay.Client(auth=("rzp_test_AXFywgHwKPNQqd","5yJOuwZu7vhT9llQwhxmDCXi"))
        order_amount = int(request.data['amount']) * 100
       
        order_currency = 'INR'
        notes = {'shipping address':request.data['shippingaddress'],'billing address':request.data['billingaddress']}
        order_receipt = request.data['reciept']
        

        payment = client.order.create({'amount':order_amount, 'currency':'INR','notes':notes, 'receipt':order_receipt,'payment_capture':'1'})
        
        newpay = RazorPayPayment.objects.create(user=request.user,razorpay_order_id=payment['id'],amount=payment['amount']/100)
        
        return Response(data=payment)

class PaymentOrderVerify(generics.GenericAPIView):
    serializer_class = VerifyPaymentOrder

    def generate_pdf(self):
        report = RazorPayPayment.objects.all()
        template_path = 'profile_brand_report.html'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Report.pdf"'

        html = render_to_string(template_path, {'report': report})
        

        pisaStatus = pisa.CreatePDF(html, dest=response)

        return response

    def post(self, request):
        client = razorpay.Client(auth=("rzp_test_AXFywgHwKPNQqd","5yJOuwZu7vhT9llQwhxmDCXi"))

        order_id = request.data['order_id']

        
        
        try:
            newpay = RazorPayPayment.objects.get(razorpay_order_id=request.data['order_id'])
            resp = client.order.fetch(order_id)
            bbb = self.generate_pdf()
            
            return bbb
            # return Response(data=resp)
        except RazorPayPayment.DoesNotExist:
            return Response({"error":"This is Not Valid Order"})

        
        

class PaymentOrderUpdate(generics.GenericAPIView):
    serializer_class = UpdatePaymentOrder

    def get(self, request, id):
        try:
            queryset = RazorPayPayment.objects.get(razorpay_order_id=id)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        except RazorPayPayment.DoesNotExist:
            return Response({"Error":"This Is Not Valid Order"})
    def patch(self, request, id):
        
        queryset = RazorPayPayment.objects.get(razorpay_order_id=id)

        queryset.status = request.data['status']
        queryset.save()
        
        serializer = self.get_serializer(queryset)
        

        return Response(serializer.data)

class PaymentOrderDelete(generics.GenericAPIView):
    serializer_class = UpdatePaymentOrder

    def delete(self, request, id):
        queryset = RazorPayPayment.objects.get(razorpay_order_id=id).delete()

        return Response({"Message":"Delete Succesfully"})


class PaymentOrderStatus(generics.GenericAPIView):
    serializer_class = UpdatePaymentOrder

    def get(self, request, id):
        try:
            queryset = RazorPayPayment.objects.get(razorpay_order_id=id)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        except RazorPayPayment.DoesNotExist:
            return Response({"Error":"This Is Not Valid Order"})



class PaymentOrderSearch(generics.ListAPIView):
    queryset = RazorPayPayment.objects.all()
    serializer_class = UpdatePaymentOrder
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    pagination_class.page_size_query_param = 'limit'
    search_fields = ['name']