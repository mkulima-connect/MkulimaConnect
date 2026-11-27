from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Subscription


@login_required
def subscribe(request):
    current = Subscription.objects.filter(user=request.user, active=True).order_by("-started_at").first()
    return render(request, "subscriptions/subscribe.html", {"current": current, "plans": Subscription.PLAN_CHOICES})


@login_required
@require_POST
def activate_subscription(request):
    plan = request.POST.get("plan", Subscription.PLAN_BASIC)
    if plan not in dict(Subscription.PLAN_CHOICES):
        messages.error(request, "Invalid plan.")
        return redirect("subscriptions:subscribe")
    Subscription.objects.filter(user=request.user, active=True).update(active=False)
    sub = Subscription(user=request.user, plan=plan)
    sub.activate(plan=plan)
    messages.success(request, f"{sub.get_plan_display()} subscription activated.")
    return redirect("subscriptions:subscribe")
