import base64
import hashlib
import json
import os

import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def get_tpay_url(
    total_cost: str,
    order_description: str,
    crc: str,
    shipping_name: str,
    shipping_email: str,
    result_url: str,
    return_url: str,
) -> str:
    """
    This function generates a Tpay link.

    Args:
        total_cost (str): The total cost of the order.
        order_description (str): The description of the order.
        crc (str): The cyclic redundancy check value.
        shipping_name (str): The name for the shipping address.
        shipping_email (str): The email for the shipping address.
        result_url (str): The result URL after the payment.
        return_url (str): The return URL after the payment.

    Returns:
        str: The generated Tpay link.
    """

    merchant_id = os.environ.get('EVENT_TOOL_TPAY_MERCHANT_ID')
    merchant_security_code = os.environ.get('EVENT_TOOL_TPAY_MERCHANT_SECURITY_CODE')

    md5_calc_str = f'{merchant_id}&{total_cost}&{crc}&{merchant_security_code}'

    md5_hash = hashlib.md5(md5_calc_str.encode('utf-8'), usedforsecurity=False)
    md5sum = md5_hash.hexdigest()

    tpay_link = (
        f'https://secure.tpay.com/?id={merchant_id}&amount={total_cost}&description={order_description}'
        f'&crc={crc}&name={shipping_name}&email={shipping_email}&result_url={result_url}'
        f'&return_url={return_url}&md5sum={md5sum}'
    )
    tpay_link = tpay_link.replace(' ', '%20')

    return tpay_link


def base64_urlsafe_decode(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return base64.urlsafe_b64decode(data)


def is_tpay_request(request):
    # Valid data from tpay.com
    body = request.body
    jws = request.headers.get('X-JWS-Signature')
    if not jws:
        return False

    jws_data = jws.split('.')
    headers, signature = jws_data[0], jws_data[2]

    if not headers or not signature:
        return False

    headers_json = base64_urlsafe_decode(headers).decode('utf-8')
    headers_dict = json.loads(headers_json)

    x5u = headers_dict.get('x5u')
    if not x5u:
        return False

    if 'https://secure.tpay.com' not in x5u:
        return False

    # Get certificates from tpay.com
    certificate_response = requests.get(x5u)
    certificate_text = certificate_response.text
    certificate = x509.load_pem_x509_certificate(certificate_text.encode(), default_backend())

    ca_certificiate_response = requests.get('https://secure.tpay.com/x509/tpay-jws-root.pem')
    ca_certificate_text = ca_certificiate_response.text
    ca_certificate = x509.load_pem_x509_certificate(ca_certificate_text.encode(), default_backend())

    # Verify JWS sign certificate with Tpay CA certificate
    try:
        ca_certificate.public_key().verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificate.signature_hash_algorithm,
        )
    except Exception:
        return False

    # Verify JWS signature
    payload = base64.urlsafe_b64encode(body).rstrip(b'=').decode()
    decoded_signature = base64_urlsafe_decode(signature)

    try:
        certificate.public_key().verify(
            decoded_signature, f'{headers}.{payload}'.encode(), padding.PKCS1v15(), hashes.SHA256()
        )
    except Exception:
        return False

    return True
