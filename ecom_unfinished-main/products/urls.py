from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='all'),
    path('item/<slug:slug>/', views.ProductDetailView.as_view(), name='single'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
]
