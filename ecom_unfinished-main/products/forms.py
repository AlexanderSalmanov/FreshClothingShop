from django import forms

from .models import Product, Category

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'brand', 'category', 'price', 'image', 'description']
