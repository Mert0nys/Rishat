import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Item
import os

stripe.api_key = os.getenv('SECRET_KEY')

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://localhost:8000/success/',
        cancel_url='https://localhost:8000/cancel/',
    )
    
    return JsonResponse({'id': session.id})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html', {'item': item})
