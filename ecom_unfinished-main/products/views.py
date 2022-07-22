from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from carts.models import Cart
from .models import Product, Category
from .forms import ProductForm
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


class ProductCreate(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products:all')

    def form_valid(self, form):
        request = self.request
        user_obj = request.user
        instance = form.save(commit=False)
        if request.FILES.get('image', None) is not None:
            instance.image = request.FILES['image']
        instance.seller = user_obj
        instance.save()
        return super().form_valid(form)

@login_required
def delete_product(self, slug):
    product_obj = get_object_or_404(Product, slug=slug)
    product_obj.delete()
    return redirect('products:all')
