from django.urls import path
from .views import (OrderSubmitView, OrderIndexView,
                    OrderReceiptView, OrderSettleView,
                    OrderCreditView)

urlpatterns = [
    path('', OrderIndexView.as_view(), name='index'),
    path('submit/', OrderSubmitView.as_view(), name='submit'),
    path('settle/', OrderSettleView.as_view(), name='settle'),
    path('credit/', OrderCreditView.as_view(), name='credit'),
    path('receipt/', OrderReceiptView.as_view(), name='receipt')
]
