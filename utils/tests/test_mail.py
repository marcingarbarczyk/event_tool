from unittest import TestCase
from unittest.mock import patch

from django.core import mail
from django.test import override_settings

from utils.mail import send_message_via_email


class TestEmailFunction(TestCase):
    @override_settings(DEFAULT_FROM_EMAIL='from@example.com')
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('utils.mail.render_to_string', return_value='<h1>Test html message</h1>')
    @patch('utils.mail.strip_tags', return_value='Test plain message')
    def test_send_message_via_email(self, mock_strip_tags, mock_render_to_string):
        subject = 'Test Subject'
        template = 'your_template.html'
        context = {'key': 'value'}
        to = ['to@example.com']

        send_message_via_email(subject, template, context, to)

        mock_render_to_string.assert_called_once_with(template, context)
        mock_strip_tags.assert_called_once_with(mock_render_to_string.return_value)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
