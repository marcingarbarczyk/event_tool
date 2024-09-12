from typing import Dict, List

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_message_via_email(subject: str, template: str, context: Dict, to: List[str]) -> None:
    """
    Sends an email to a set of recipients.

    Args:
        subject (str): The subject of the email.
        template (str): The template to use for the email body.
        context (Dict): A dictionary containing context for the template rendering.
        to (List[str]): A list of recipient email addresses.

    Returns:
        None
    """
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, to, html_message=html_message)
