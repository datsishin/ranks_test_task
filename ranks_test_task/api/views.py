import os
import stripe
import dotenv

from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from rest_framework import viewsets, status

from .models import Item, Order
from .serializers import OrderSerializer

dotenv.load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

YOUR_DOMAIN = 'http://127.0.0.1:8000'


class ProductCheckoutPageView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    first_template = 'page_with_item.html'
    second_template = 'page_with_two_items.html'
    serializer_class = OrderSerializer

    def get_product_page(self, request, id: int = None):
        if id:
            item = get_object_or_404(self.queryset, id=id)
            data = {'item': item}
            return render(request, self.first_template, context=data)
        first_item = get_object_or_404(self.queryset, id=1)
        second_item = get_object_or_404(self.queryset, id=2)
        data = {'first_item': first_item, 'second_item': second_item}
        return render(request, self.second_template, context=data)

    # def add_to_order(self, id: int):
    #     item = get_object_or_404(self.queryset, id=id)
    #     serializer = self.serializer_class(products=item)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return serializer.data(status=status.HTTP_201_CREATED)
    #     return serializer.errors(status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSessionView(View):
    queryset = Item.objects.all()

    def post(self, request, id: int):
        item = get_object_or_404(self.queryset, id=id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],

            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)
