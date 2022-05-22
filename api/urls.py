from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('item', views.ItemViewSet, basename='items')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/buy/<int:id>/', views.BuyItemView.as_view(), name='buy_item'),
    path('v1/success/', views.SuccessView.as_view(), name='success'),
    path('v1/cancel/', views.CancelView.as_view(), name='cancel')
]
