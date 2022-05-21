from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('item', views.ItemViewSet, basename='items')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/buy/<int:id>/', views.BuyItemViewSet.as_view(), name='buy_item')
]
