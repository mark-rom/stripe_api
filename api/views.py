import logging
import sys

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import views
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from invoices import models

from . import serializers

stripe.api_key = settings.STRIPE_API_KEY

log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s, %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
log.setLevel(logging.ERROR)
log.addHandler(handler)


class ItemViewSet(GenericViewSet, RetrieveModelMixin):
    """Вьюсет для модели Item.
    Допускает исполнение только Retrieve операций,
    передает данные на эндпойнт item/<id>/
    и рендерит соответствующую страницу."""

    http_method_names = ['get']
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'invoices/item_page.html'


class BuyItemView(views.APIView):
    """Вью-функция для получения сессии оплаты Stripe.
    Допускает только GET метод, возвращает id Stripe-сессии.
    """

    allowed_methods = ['get']

    def get(self, request, id):
        item = get_object_or_404(models.Item, pk=id)
        try:
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
                        'unit_amount_decimal': item.price,
                    },
                    'quantity': 1
                }]
            )
        except stripe.error.CardError as e:
            log.error("Ошибка метода оплаты: {}".format(e.user_message))
        except stripe.error.InvalidRequestError:
            log.error("Неверный запрос")
        except Exception:
            log.error('Произошла ошибка. Возможно она связана со Stripe.')

        return Response({'message': 'Got session_id', 'id': session.id})


class SuccessView(TemplateView):
    """Вью-функция для рендера страницы успешной оплаты."""

    template_name = 'static/success.html'


class CancelView(TemplateView):
    """Вью-функция для рендера страницы отмены оплаты."""

    template_name = 'static/cancel.html'
