import os
import unittest
from unittest.mock import patch

from utils.tpay import get_tpay_url


class TestGetTpayUrl(unittest.TestCase):
    @patch.dict(os.environ, {'EVENT_TOOL_TPAY_MERCHANT_ID': '1', 'EVENT_TOOL_TPAY_MERCHANT_SECURITY_CODE': 's3cr3t'})
    def test_get_tpay_url(self):
        total_cost = '100'
        order_description = 'Order description'
        crc = 'order1'
        shipping_name = 'Shopper Name'
        shipping_email = 'shopper@example.com'
        result_url = 'https://example.com/result'
        return_url = 'https://example.com/return'

        expected_url = 'https://secure.tpay.com/?id=1&amount=100&description=Order%20description&crc=order1&name=Shopper%20Name&email=shopper@example.com&result_url=https://example.com/result&return_url=https://example.com/return&md5sum=74354612c5d473af4cd4a3bdc8de1681'
        actual_url = get_tpay_url(
            total_cost, order_description, crc, shipping_name, shipping_email, result_url, return_url
        )

        self.assertEqual(actual_url, expected_url)
