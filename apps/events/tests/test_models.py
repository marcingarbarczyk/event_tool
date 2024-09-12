from datetime import timedelta

from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.events.models import Counter, Event, Registration


class EventSetupTestMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.event_past = Event.objects.create(
            name='Example event',
            date_start=timezone.now().date() - timedelta(days=10),
        )
        cls.event_future = Event.objects.create(
            name='Example event',
            date_start=timezone.now().date() + timedelta(days=10),
        )
        cls.counter_event_future_1 = Counter.objects.create(
            title='My example counter #1',
            value='10',
        )
        cls.counter_event_future_2 = Counter.objects.create(
            title='My example counter #2',
            value='20',
        )
        cls.event_future.counters.add(cls.counter_event_future_1, through_defaults={})
        cls.event_future.counters.add(cls.counter_event_future_2, through_defaults={})
        cls.event_future.refresh_from_db()


class TestEventModel(EventSetupTestMixin):
    def test_order_queryset(self):
        self.assertEqual(list(Event.objects.all()), [self.event_past, self.event_future])

    def test_max_registrations_property(self):
        self.event_future.max_registrations = 3
        self.event_future.save()
        self.assertEqual(self.event_future.registrations_remaining_count, 3)

        Registration.objects.create(
            name='Test 1',
            email='test1@test.com',
            is_paid=False,
            event=self.event_future,
        )
        Registration.objects.create(
            name='Test 2',
            email='test2@test.com',
            is_paid=True,
            event=self.event_future,
        )
        self.assertEqual(self.event_future.registrations_remaining_count, 2)
        Registration.objects.create(
            name='Test 3',
            email='test3@test.com',
            is_paid=True,
            event=self.event_future,
        )
        Registration.objects.create(
            name='Test 4',
            email='test4@test.com',
            is_paid=True,
            event=self.event_future,
        )
        self.assertEqual(self.event_future.registrations_remaining_count, 0)
        Registration.objects.create(
            name='Test 5',
            email='test5@test.com',
            is_paid=True,
            event=self.event_future,
        )
        self.assertEqual(self.event_future.registrations_remaining_count, 0)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
@override_settings(NEW_REGISTRATIONS_EMAIL_RECEIVERS=['jonh@example.com', 'jane@example.com'])
class TestRegistrationModel(EventSetupTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.registration = Registration.objects.create(
            name='John',
            email='johndoe@example.com',
            unique_code='PURCK8FR',
            event=cls.event_future,
        )

    def setUp(self):
        mail.outbox = []

    def test_store_responses_static_method(self):
        initial_data = {
            'name': 'John',
            'email': 'johndoe@example.com',
            'form_id': 'PURCK8FR',
            'data1': 'data1',
            'data2': 'data2',
            'data3': 'data3',
            'data4': 'data4',
            'data5': 'data5',
        }
        parsed_data = Registration.store_responses(initial_data)
        self.assertEqual(parsed_data, 'data1\ndata2\ndata3\ndata4\ndata5\n')

    def test_send_registration_email_notification(self):
        registration_2 = Registration.objects.create(
            name='Jane',
            email='janedoe@example.com',
            unique_code='P342K8FR',
            event=self.event_future,
        )
        self.assertEqual(mail.outbox[0].subject, 'Potwierdzenie zgłoszenia')
        self.assertEqual(mail.outbox[0].to, [registration_2.email])
        self.assertIn('Status płatności możesz zweryfikować klikając w poniższy link', mail.outbox[0].body)

    # def test_send_new_paid_registration_email_notification(self):
    #     self.registration.send_new_paid_registration_email_notification()
    #     self.assertEqual(mail.outbox[0].subject, 'Nowe zgłoszenie do konferencji zostało opłacone')
    #     self.assertEqual(mail.outbox[0].to, ['jonh@example.com', 'jane@example.com'])
    #     self.assertIn('Nowe zgłoszenie', mail.outbox[0].body)

    def test_send_successful_payment_email_notification(self):
        self.registration.send_successful_payment_email_notification()
        self.assertEqual(mail.outbox[0].subject, 'Wstęp na wydarzenie został opłacony')
        self.assertEqual(mail.outbox[0].to, [self.registration.email])
        self.assertIn('Płatność za wydarzenie została potwierdzona', mail.outbox[0].body)
