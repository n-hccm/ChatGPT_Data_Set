# ecommerce/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, UserPoints
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if product not in cart.products.all():
        cart.products.add(product)
        cart.calculate_total()
        messages.success(request, "Added to cart successfully!")

    return redirect('home')


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})
