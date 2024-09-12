from apps.events.models import Registration
from apps.events.tests.test_models import EventSetupTestMixin
from apps.events.utils import generate_unique_code


class TestGenerateUniqueCode(EventSetupTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.registration_1 = Registration.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            event=cls.event_future,
        )
        cls.registration_2 = Registration.objects.create(
            name='Jane Doe',
            email='janedoe@example.com',
            event=cls.event_future,
        )

    def test_generate_unique_code(self):
        code = generate_unique_code()
        self.assertNotEqual(code, self.registration_1.unique_code)
        self.assertNotEqual(code, self.registration_2.unique_code)
        self.assertEqual(len(code), 20)
        codes = set()
        for _ in range(1000):
            code = generate_unique_code()
            self.assertNotIn(code, codes)
            self.assertEqual(len(code), 20)
            codes.add(code)
