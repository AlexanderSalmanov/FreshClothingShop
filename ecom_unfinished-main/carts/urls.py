from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('home/', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('remove/', views.cart_remove, name='remove'),
    path('checkout/', views.checkout_home, name='checkout_home')
]
