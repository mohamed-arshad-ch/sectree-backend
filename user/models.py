from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
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
    otp_code = models.CharField(max_length=150,blank=True)
    active = models.BooleanField(default=True)
    email = models.EmailField(unique=True,blank=True)



    def __str__(self):
        return self.username

# class Item(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.FloatField()
#     discount_price = models.FloatField(blank=True, null=True)
#     category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
#     label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    
#     description = models.TextField()
#     image = models.ImageField()

#     def __str__(self):
#         return self.title

    


# class OrderItem(models.Model):
#     user = models.ForeignKey(CustomUser,
#                              on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title}"

#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def get_total_discount_item_price(self):
#         return self.quantity * self.item.discount_price

#     def get_amount_saved(self):
#         return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.item.discount_price:
#             return self.get_total_discount_item_price()
#         return self.get_total_item_price()


# class Order(models.Model):
#     user = models.ForeignKey(CustomUser,
#                              on_delete=models.CASCADE)
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     items = models.ManyToManyField(OrderItem)
#     start_date = models.DateTimeField(auto_now_add=True)
    
#     ordered = models.BooleanField(default=False)
#     shipping_address = models.ForeignKey(
#         'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
#     billing_address = models.ForeignKey(
#         'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
   
    
#     being_delivered = models.BooleanField(default=False)
#     received = models.BooleanField(default=False)
#     refund_requested = models.BooleanField(default=False)
#     refund_granted = models.BooleanField(default=False)

#     '''
#     1. Item added to cart
#     2. Adding a billing address
#     (Failed checkout)
#     3. Payment
#     (Preprocessing, processing, packaging etc.)
#     4. Being delivered
#     5. Received
#     6. Refunds
#     '''

#     def __str__(self):
#         return self.user.username

#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_total_item_price()
        
#         return total


# class Address(models.Model):
#     user = models.ForeignKey(CustomUser,
#                              on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=100)
#     apartment_address = models.CharField(max_length=100)
    
#     zipc = models.CharField(max_length=100)
#     address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
#     default = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name_plural = 'Addresses'


# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(CustomUser,
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     order = models.ForeignKey(Order,
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.amount

class RazorPayPayment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    def __str__(self):
        return self.razorpay_order_id