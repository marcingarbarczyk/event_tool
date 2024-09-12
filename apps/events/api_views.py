from _decimal import Decimal
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.events.models import Registration
from utils.tpay import is_tpay_request


class TPayNotificationReceiver(APIView):
    """
    View for receiving payment notification from tpay.com
    """

    authentication_classes = []
    permission_classes = []

    def get_object(self, code):
        return Registration.objects.filter(unique_code=code).first()

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        if is_tpay_request(request):
            tpay_response = request.POST.dict()

            try:
                transaction_status = tpay_response['tr_status']
                paid_amount = tpay_response['tr_paid']
                error = tpay_response['tr_error']
                crc = tpay_response['tr_crc']
            except KeyError:
                return HttpResponse('FALSE - Invalid request', content_type='text/plain')

            registration = self.get_object(crc)
            if registration is None:
                return HttpResponse('FALSE - Order {} not exist'.format(crc))
            registration.tpay_notification = tpay_response

            if transaction_status == 'TRUE' and error == 'none':
                paid_amount = Decimal(paid_amount)
                registration.paid_amount = paid_amount
                registration.is_paid = True
                registration.send_new_paid_registration_email_notification()
                registration.send_successful_payment_email_notification()

            registration.save()
            return HttpResponse('TRUE', content_type='text/plain')
        else:
            return HttpResponse('FALSE - Not authorized', content_type='text/plain')
