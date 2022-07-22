from django.shortcuts import render
from django.views import generic
from django.db.models import Max
from django.urls import reverse

from products.models import Product

# Create your views here.

class SearchListView(generic.ListView):
    model = Product
    template_name = 'search/search_list.html'
    context_object_name = 'results'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        return Product.objects.search(query)

class PriceRangeListView(generic.ListView):
    model = Product
    template_name = 'search/price_range_list.html'
    paginate_by = 6


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        context['top_range'] = request.GET.get('top_range')
        context['lower_range'] = request.GET.get('lower_range')
        if context['lower_range'] == '':
            context['lower_range'] = 0
        if context['top_range'] == '':
            context['top_range'] = Product.objects.aggregate(Max('price'))['price__max']
        context['product_list'] = Product.objects.filter(price__gte=context['lower_range'], price__lte=context['top_range'])
        return context

class OrderedListView(generic.ListView):
    model = Product
    template_name = 'search/ordered_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        context['price_order'] = request.GET.get('price_order', None)
        if context['price_order'] is not None:
            if context['price_order'] == 'ascend':
                context['product_list'] = Product.objects.all().order_by('price')
            elif context['price_order'] == 'descend':
                context['product_list'] = Product.objects.all().order_by('-price')
            else:
                context['product_list'] = Product.objects.all()
        context['time_order'] = request.GET.get('time_order', None)
        if context['time_order'] is not None:
            if context['time_order'] == 'recent':
                context['product_list'] = Product.objects.all().order_by('-timestamp')
            elif context['time_order'] == 'oldest':
                context['product_list'] = Product.objects.all().order_by('timestamp')
            else:
                context['product_list'] = Product.objects.all()
        context['popularity_order'] = request.GET.get('popularity_order', None)
        if context['popularity_order'] is not None:
            if context['popularity_order'] == 'mp':
                context['product_list'] = Product.objects.order_by('-times_viewed')
            elif context['popularity_order'] == 'lp':
                context['product_list'] = Product.objects.order_by('times_viewed')
            else:
                context['product_list'] = Product.objects.all()

        return context
