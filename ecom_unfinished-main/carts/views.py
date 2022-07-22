from django.shortcuts import render, redirect
from django.http import JsonResponse

from products.models import Product
from .models import Cart
from accounts.forms import GuestForm, LoginForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from orders.models import Order
# Create your views here.

def cart_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)

    return render(request, 'carts/cart_home.html', {'cart': cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id', None)
    added = False
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('carts:home')
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            added = False
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()

    if request.is_ajax:
        print('ajax request')
        json = {
            'added': added,
            'removed': not added,
            'cart_items': request.session['cart_items']
        }
        return JsonResponse(json)

    return redirect('carts:home')

def cart_remove(request):
    product_id = request.POST.get('product_id', None)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)

        cart_obj.products.remove(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    if request.is_ajax:
        json = {
            'cart_items': cart_obj.products.count(),
            'cart_total_price': cart_obj.total,
            'cart_subtotal': cart_obj.subtotal,
        }
        return JsonResponse(json)
    return redirect('carts:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    guest_form = GuestForm()
    login_form = LoginForm()

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(request, billing_profile=billing_profile, cart_obj=cart_obj)


    print(cart_obj.total)
    context = {
        'guest_form': guest_form,
        'login_form': login_form,
        'billing_profile': billing_profile,
        'order': order_obj
                }
    return render(request, 'carts/checkout_home.html', context)
