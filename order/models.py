from django.db import models
from users.models import User
from store.models import Product
from utils.models import Color, Size, State, City


class Order(models.Model):
    STATUS = (('PAD', 'پرداخت شده'),
              ('PRP', 'در حال آماده سازی'),
              ('PST', 'ارسال شده'),
              ('DLV', 'تحویل داده شده'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS, max_length=20, default='پرداخت شده')
    paid_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(blank=True)
    delivered_at = models.DateTimeField(blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=50)
    image = models.CharField(max_length=70)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    qty = models.PositiveIntegerField()


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='address')
    state = models.ForeignKey(State, related_name='address', on_delete=models.RESTRICT)
    city = models.ForeignKey(City, related_name='address', on_delete=models.RESTRICT)
    detail = models.TextField(max_length=700)
    post_code = models.IntegerField()
    shipping_price = models.IntegerField()
    phone_number = models.CharField(max_length=200)
# Create your models here.
