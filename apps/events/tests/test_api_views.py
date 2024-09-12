from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from apps.events.tests.test_models import EventSetupTestMixin


class TPayNotificationReceiver(EventSetupTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = APIClient()
        cls.url = reverse('tpay_payment')
        cls.user = User.objects.create_user(username='test', password='test')  # noqa

    # TODO: tests required!
    # def test_tpay_noficiation_ip_permissions(self):
    #     response_1 = self.client.post(self.url, {})
    #
    #     with mock.patch('apps.events.api_views.get_ip') as get_ip_mock:
    #         get_ip_mock.return_value = '195.149.229.109'
    #         response_2 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #         get_ip_mock.return_value = '148.251.96.163'
    #         response_3 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #         get_ip_mock.return_value = '178.32.201.77'
    #         response_4 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #         get_ip_mock.return_value = '46.248.167.59'
    #         response_5 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #         get_ip_mock.return_value = '46.29.19.106'
    #         response_6 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #         get_ip_mock.return_value = '176.119.38.175'
    #         response_7 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #
    #     self.assertEqual(response_1.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_2.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_3.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_4.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_5.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_6.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_7.status_code, status.HTTP_200_OK)
    #     self.assertContains(response_1, 'FALSE - Not authorized')
    #     self.assertContains(response_2, 'FALSE - Invalid request')
    #     self.assertContains(response_3, 'FALSE - Invalid request')
    #     self.assertContains(response_4, 'FALSE - Invalid request')
    #     self.assertContains(response_5, 'FALSE - Invalid request')
    #     self.assertContains(response_6, 'FALSE - Invalid request')
    #     self.assertContains(response_7, 'FALSE - Invalid request')
    #
    # def test_tpay_notification_auth(self):
    #     response_1 = self.client.post(self.url, {})
    #     response_2 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #
    #     self.assertEqual(response_1.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_2.status_code, status.HTTP_200_OK)
    #     self.assertContains(response_1, 'FALSE - Not authorized')
    #     self.assertContains(response_2, 'FALSE - Invalid request')
    #
    # def test_tpay_notification_correct_data(self):
    #     registration = Registration.objects.create(
    #         event=self.event_future,
    #         email='johndoe@example.com',
    #         name='John Doe',
    #     )
    #     data_1 = {
    #         'tr_status': 'TRUE',
    #         'tr_error': 'none',
    #         'tr_paid': '100.00',
    #         'tr_crc': registration.unique_code,
    #     }
    #     data_2 = {
    #         'tr_status': 'TRUE',
    #         'tr_error': 'none',
    #         'tr_paid': '100.00',
    #         'tr_crc': 'WRONG_UNIQUE_CODE',
    #     }
    #     response_1 = self.client.post(self.url, data_1, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response_2 = self.client.post(self.url, data_2, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response_3 = self.client.post(self.url, {}, HTTP_AUTHORIZATION='Token ' + self.token.key)
    #
    #     self.assertEqual(response_1.status_code, status.HTTP_200_OK)
    #     self.assertContains(response_1, 'TRUE')
    #     self.assertEqual(response_2.status_code, status.HTTP_200_OK)
    #     self.assertContains(response_2, 'FALSE - Order WRONG_UNIQUE_CODE not exist')
    #     self.assertEqual(response_3.status_code, status.HTTP_200_OK)
    #     self.assertContains(response_3, 'FALSE - Invalid request')
