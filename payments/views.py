from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator

from products.models import Product


@login_required
def process_payment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse({'status': 'pending', 'product_id': product.id, 'amount': str(product.price)})


@method_decorator(login_required, name='dispatch')
class PaymentInitiateView(View):
    def post(self, request):
        return JsonResponse({'status': 'initiated'})


class PaymentCallbackView(View):
    def post(self, request):
        return JsonResponse({'status': 'received'})

    def get(self, request):
        return JsonResponse({'status': 'received'})
