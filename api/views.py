from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

import stripe

from invoices import models
from . import serializers

stripe.api_key = settings.STRIPE_API_KEY


class ItemViewSet(ModelViewSet):
    # сделать миксином только Retrieve
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'test_template.html'


class BuyItemViewSet(APIView):

    def get(self, request, id):
        item = get_object_or_404(models.Item, pk=id)
        session = stripe.checkout.Session.create(
            mode='payment',
            success_url='http://127.0.0.1:8000/api/v1/success',
            cancel_url='http://127.0.0.1:8000/api/v1/cancel',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1
            }]
        )

        return Response({'message': 'session_id', 'id': session.id})
