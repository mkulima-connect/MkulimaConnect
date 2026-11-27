from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def subscribe(request):
    return render(request, 'subscriptions/subscribe.html')
