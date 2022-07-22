from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.SearchListView.as_view(), name='query'),
    path('range/', views.PriceRangeListView.as_view(), name='price'),
    path('ordering/', views.OrderedListView.as_view(), name='order')
]
