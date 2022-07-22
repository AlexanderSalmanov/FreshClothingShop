from .models import Category, Product
from .forms import ProductForm

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def product_add_form(request):
    return {
        'product_form': ProductForm(request.POST or None)
    }
