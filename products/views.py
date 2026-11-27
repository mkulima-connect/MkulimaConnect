from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import ProductForm, ReviewForm
from .models import Product


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:product_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'form': form})


@login_required
@role_required(['farmer'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})
