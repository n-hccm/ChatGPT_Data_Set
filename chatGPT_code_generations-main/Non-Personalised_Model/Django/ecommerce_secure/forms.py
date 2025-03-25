# ecommerce/forms.py
from django import forms
from .models import Product

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
