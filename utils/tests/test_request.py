from django.test import RequestFactory, TestCase

from utils.request import get_ip


class GetIPTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_ip(self):
        request = self.factory.get('/')
        request.META = {'HTTP_X_FORWARDED_FOR': '123.123.123.123', 'REMOTE_ADDR': '123.123.123.123'}

        self.assertEqual(get_ip(request), '123.123.123.123')
