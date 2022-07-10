from .models import Category, Product

def categories(request):
    return {
        'categories': Category.objects.all()
    }
