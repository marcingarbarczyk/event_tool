import random
from datetime import date, timedelta
from io import BytesIO

import factory
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.backends.postgresql.psycopg_any import DateRange
from factory import Iterator, SubFactory, lazy_attribute
from factory.django import DjangoModelFactory, ImageField
from faker import Faker
from PIL import Image

from ..dynamo_forms.models import Form
from .models import (
    Counter,
    Event,
    EventBundle,
    EventBundleCodeDiscount,
    EventBundlePrice,
    EventCounter,
    EventPartner,
    EventPlanItem,
    EventSpeaker,
    News,
    Partner,
    Photo,
    Registration,
    Speaker,
    Video,
)

User = get_user_model()


def generate_blank_image(width=200, height=200, color=(128, 128, 128)):
    image = Image.new('RGB', (width, height), color)
    thumb_io = BytesIO()
    image.save(thumb_io, format='JPEG')
    return ContentFile(thumb_io.getvalue(), 'speakers/blank_image.jpg')


def random_text(min_length, max_length):
    faker = Faker()
    text = ''
    while len(text) < min_length:
        text += faker.text(max_nb_chars=max_length)
    return text[:max_length]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


class StaffUserFactory(UserFactory):
    is_staff = True


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker(
        'text',
        max_nb_chars=100,
    )
    introduction = factory.Faker(
        'text',
        max_nb_chars=100,
    )
    description = factory.Faker(
        'text',
        max_nb_chars=200,
    )
    additional_description = factory.Faker(
        'text',
        max_nb_chars=200,
    )
    footer_text = factory.Faker(
        'text',
        max_nb_chars=200,
    )
    partners_text = factory.Faker(
        'text',
        max_nb_chars=20,
    )
    max_registrations = 100
    privacy_policy = factory.Faker(
        'text',
        max_nb_chars=1000,
    )
    privacy_policy_checkbox = factory.Faker(
        'text',
        max_nb_chars=100,
    )
    regulations = factory.Faker(
        'text',
        max_nb_chars=1000,
    )
    form = Iterator(Form.active_objects.all())
    date_start = factory.Faker('future_date', end_date='+30d')
    logo = factory.LazyAttribute(
        lambda _: generate_blank_image(
            width=140,
            height=50,
        )
    )
    facebook_link = factory.Faker('url')
    tiktok_link = factory.Faker('url')
    youtube_link = factory.Faker('url')
    instagram_link = factory.Faker('url')
    x_link = factory.Faker('url')
    background_image = ImageField()
    city = factory.Faker('city')
    address = factory.Faker('address')
    place = factory.Faker(
        'sentence',
    )

    @factory.lazy_attribute
    def promo_movie_html(self):
        return '<iframe width="560" height="315" src="https://www.youtube.com/embed/yECaluBLmtg?si=v6Bte1vX8_HFf7YG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'


class SpeakerFactory(DjangoModelFactory):
    class Meta:
        model = Speaker

    name = factory.Faker('name')
    description = factory.Faker(
        'text',
        max_nb_chars=100,
    )
    image = factory.LazyAttribute(lambda _: generate_blank_image())
    facebook_link = factory.Faker('url')
    tiktok_link = factory.Faker('url')
    youtube_link = factory.Faker('url')
    instagram_link = factory.Faker('url')
    x_link = factory.Faker('url')


class CounterFactory(DjangoModelFactory):
    class Meta:
        model = Counter

    title = factory.Faker('sentence')
    value = factory.Faker('random_int')


class EventSpeakerFactory(DjangoModelFactory):
    class Meta:
        model = EventSpeaker

    event = Iterator(Event.objects.all())
    speaker = Iterator(Speaker.objects.all())


class EventBundleFactory(DjangoModelFactory):
    class Meta:
        model = EventBundle

    name = factory.Faker('sentence')
    event = Iterator(Event.objects.all())
    description = """
    <ul>
        <li>Item #1</li>
        <li>Item #2</li>
        <li>Item #3</li>
        <li>Item #4</li>
        <li>Item #5</li>
    </ul>
    """
    is_sold_out = False
    is_featured = factory.Faker('boolean')


class EventBundlePriceFactory(DjangoModelFactory):
    class Meta:
        model = EventBundlePrice

    title = factory.Faker('word')
    price = factory.Faker('random_int')
    event_bundle = Iterator(EventBundle.objects.all())
    activity_range = factory.LazyFunction(lambda: DateRange(date.today(), date.today() + timedelta(days=30)))


class EventBundleCodeDiscountFactory(DjangoModelFactory):
    class Meta:
        model = EventBundleCodeDiscount

    code = factory.Faker('word')
    event_bundle = SubFactory(EventBundleFactory)
    discount = factory.Faker('random_int')


class PartnerFactory(DjangoModelFactory):
    class Meta:
        model = Partner

    name = factory.Faker('company')
    image = factory.LazyAttribute(
        lambda _: generate_blank_image(
            width=200,
            height=90,
        )
    )
    url = factory.Faker('url')


class EventPartnerFactory(DjangoModelFactory):
    class Meta:
        model = EventPartner

    event = SubFactory(EventFactory)
    partner = SubFactory(PartnerFactory)


class EventCounterFactory(DjangoModelFactory):
    class Meta:
        model = EventCounter

    event = Iterator(Event.objects.all())
    counter = Iterator(Counter.objects.all())


class EventPlanItemFactory(DjangoModelFactory):
    class Meta:
        model = EventPlanItem

    title = factory.Faker('sentence')
    event = Iterator(Event.objects.all())
    speaker = Iterator(Speaker.objects.all())
    description = factory.Faker(
        'text',
        max_nb_chars=200,
    )


class NewsFactory(DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Faker(
        'text',
        max_nb_chars=50,
    )
    image = factory.LazyAttribute(
        lambda _: generate_blank_image(
            width=800,
            height=600,
        )
    )

    @factory.lazy_attribute
    def entry(self):
        return random_text(200, 450)

    @factory.lazy_attribute
    def description(self):
        return random_text(500, 800)


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo

    image = factory.LazyAttribute(
        lambda _: generate_blank_image(
            width=800,
            height=600,
        )
    )


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    thumbnail = factory.LazyAttribute(
        lambda _: generate_blank_image(
            width=800,
            height=600,
        )
    )

    @lazy_attribute
    def iframe_url(self):
        available_urls = [
            'https://www.youtube.com/watch?v=TXGbhniTBrU&pp=ygUQd2Ugd2lsbCByb2NrIHlvdQ%3D%3D',
            'https://www.youtube.com/watch?v=k4V3Mo61fJM&pp=ygUHZml4IHlvdQ%3D%3D',
        ]
        return random.choice(available_urls)  # noqa S311


class RegistrationFactory(DjangoModelFactory):
    class Meta:
        model = Registration

    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    name = factory.Faker('name')
    selected_bundle = SubFactory(EventBundleFactory)
    selected_code_discount = SubFactory(EventBundleCodeDiscountFactory)
    unique_code = factory.Faker('word')
    event = SubFactory(EventFactory)
