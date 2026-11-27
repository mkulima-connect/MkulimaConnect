from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, UserUpdateForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})
