from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, UserProfile
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        total_cost = product.price_in_points * quantity

        if user_profile.points >= total_cost and product.stock >= quantity:
            user_profile.points -= total_cost
            product.stock -= quantity
            user_profile.save()
            product.save()

            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_cost=total_cost
            )

            messages.success(request, "Purchase successful!")
            return redirect("product_list")
        else:
            messages.error(request, "Not enough points or stock!")
    
    return render(request, "store/checkout.html", {"product": product})
