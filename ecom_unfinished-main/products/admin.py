from django.contrib import admin

from .models import Product, Category
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    class Meta:
        model = Product

admin.site.register(Category)
