from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from apps.events.models import Event, News, Photo, Registration
from apps.events.tests.test_models import EventSetupTestMixin
from apps.events.views import RegistrationDetailView


class TestHomeView(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Test Event',
            background_image=SimpleUploadedFile('test_image.jpg', content=b'\x00\x01\x02\x03'),
        )
        self.news = News.objects.create(
            title='Test News',
            entry='Test News description',
            description='This is a test news',
        )
        image = SimpleUploadedFile(
            name='TestImage.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg',
        )
        self.photo = Photo.objects.create(image=image)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))  # Assuming the url name for the home view is 'home'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/home.html')

    def test_home_view_context_has_correct_data(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)
        self.assertIn(self.news, response.context['news'])
        self.assertIn(self.photo, response.context['photos'])


class TestRegulationsView(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Test Event',
            regulations='Test regulations',
        )

    def test_regulations_view_uses_correct_template(self):
        response = self.client.get(reverse('regulations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/regulations.html')

    def test_regulations_view_context_has_correct_data(self):
        response = self.client.get(reverse('regulations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['regulations'], self.event.regulations)


class TestPrivacyPolicyView(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Test Event',
            privacy_policy='Test privacy policy',
        )

    def test_privacy_policy_view_uses_correct_template(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/privacy_policy.html')

    def test_privacy_policy_view_context_has_correct_data(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['privacy_policy'], self.event.privacy_policy)


class RegistrationDetailViewTest(EventSetupTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.registration = Registration.objects.create(
            event=cls.event_future,
            name='John Doe',
            email='johndoe@example.com',
        )
        cls.url = reverse('registration_detail', args=[cls.registration.unique_code])
        cls.client = Client()
        cls.view = RegistrationDetailView()

    # def test_registration_detail_view_uses_correct_template(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'events/payment.html')

    # def test_method_allowed(self):
    #     response_post = self.client.post(self.url)
    #     response_get = self.client.get(self.url)
    #     response_put = self.client.put(self.url)
    #     response_delete = self.client.delete(self.url)
    #
    #     self.assertEqual(response_post.status_code, 302)
    #     self.assertEqual(response_get.status_code, 200)
    #     self.assertEqual(response_put.status_code, 405)
    #     self.assertEqual(response_delete.status_code, 405)

    # def test_registration_detail_view_context_has_correct_data(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context['registration'], self.registration)
    #     self.assertEqual(response.context['price'], self.event_future.active_price.price.price)
    #     self.assertIsInstance(response.context['form'], PaymentForm)

    # def test_registration_detail_view_payment_process(self):
    #     repsonse = self.client.post(self.url)
    #     self.assertEqual(repsonse.status_code, 302)

    # TODO: tests required!
