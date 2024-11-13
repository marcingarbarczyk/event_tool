from django.urls import path

from apps.events.api_views import TPayNotificationReceiver

urlpatterns = [
    path('tpay_payment/', TPayNotificationReceiver.as_view(), name='tpay_payment'),
]
