from django.shortcuts import render, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def order_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.profile.points >= product.price_in_points:
        # Deduct points
        request.user.profile.points -= product.price_in_points
        request.user.profile.save()

        # Create an order
        order = Order(user=request.user, product=product, quantity=1)
        order.save()
        return redirect('order_success')
    else:
        return redirect('insufficient_points')

def order_success(request):
    return render(request, 'shop/order_success.html')

def insufficient_points(request):
    return render(request, 'shop/insufficient_points.html')
