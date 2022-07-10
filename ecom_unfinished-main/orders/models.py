from django.db import models
from django.db.models.signals import pre_save, post_save

from ecom.utils import random_string_generator

from billing.models import BillingProfile
from carts.models import Cart

from math import fsum
# Create your models here.

class OrderManager(models.Manager):
    def new_or_get(self, request, billing_profile, cart_obj):
        order_id = request.session.get('order_id', None)
        obj = None
        qs = Order.objects.filter(
            id=order_id,
            billing_profile=billing_profile,
            cart=cart_obj
        )
        if qs.count() == 1:
            created = False
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj
            )
            created = True
            request.session['order_id'] = obj.id
        return obj, created


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    order_id = models.CharField(unique=True, max_length=255)
    # billing_address
    # shipping_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(default='created', max_length=100, choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=1.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_order_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        order_total = fsum([cart_total, shipping_total])
        formatted_total = format(order_total, '.2f')
        self.total = formatted_total
        self.save()
        return order_total

    @property
    def is_active(self):
        return self.active


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = instance.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_order_total()

post_save.connect(post_save_cart_total, sender=Cart)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = random_string_generator(15)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_order_total()

post_save.connect(post_save_order, sender=Order)
