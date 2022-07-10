from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import Http404
from django.core.paginator import Paginator

from carts.models import Cart
from .models import Product, Category
# Create your views here.


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context

    # def get_queryset(self):
    #     request = self.request
    #     price_ordering = request.GET.get('price_order', None)
    #     if price_ordering is not None:
    #         if price_ordering == 'ascend':
    #             return Product.objects.all().order_by('price')
    #         elif price_ordering == 'descend':
    #             return Product.objects.all().order_by('-price')
    #     return Product.objects.all()


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/single.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug, in_stock=True)
            instance.times_viewed += 1
            instance.save()
            print(f'{instance.title} VIEWED {instance.times_viewed} TIMES.')
        except Product.DoesNotExist:
            return Http404('Product not found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, in_stock=True)
            instance = qs.first()
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 6)
    return render(request, 'products/category_list.html', {'category': category, 'products':products, 'paginator': paginator})
