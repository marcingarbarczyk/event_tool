import factory
from factory.django import DjangoModelFactory, ImageField
from factory import SubFactory, Iterator
from django.contrib.auth import get_user_model
from .models import (
    Speaker, Bundle, Counter, EventSpeaker, EventBundle, EventBundlePrice,
    EventBundleCodeDiscount, EventPartner, EventCounter, Event, EventPlanItem,
    News, Photo, Video, Registration, Partner
)

User = get_user_model()


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker('text', max_nb_chars=100,)
    introduction = factory.Faker('text', max_nb_chars=100,)
    description = factory.Faker('text', max_nb_chars=200,)
    partners_text = factory.Faker('text', max_nb_chars=20,)
    max_registrations = 100
    privacy_policy = factory.Faker('text', max_nb_chars=1000,)
    regulations = factory.Faker('text', max_nb_chars=1000,)
    facebook_link = '#'
    tiktok_link = '#'
    youtube_link = '#'
    instagram_link = '#'
    x_link = '#'
    background_image = ImageField()
    city = factory.Faker('city')
    address = factory.Faker('address')
    place = factory.Faker('sentence',)
    # date_start = factory.Faker(get_future_datetime)


class SpeakerFactory(DjangoModelFactory):
    class Meta:
        model = Speaker

    name = factory.Faker('name')
    description = factory.Faker('text', max_nb_chars=100,)


class BundleFactory(DjangoModelFactory):
    class Meta:
        model = Bundle

    name = factory.Faker('word')


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

    event = SubFactory(EventFactory)
    bundle = SubFactory(BundleFactory)


class EventBundlePriceFactory(DjangoModelFactory):
    class Meta:
        model = EventBundlePrice

    title = factory.Faker('word')
    price = factory.Faker('random_int')


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
    url = factory.Faker('url')


class EventPartnerFactory(DjangoModelFactory):
    class Meta:
        model = EventPartner

    event = SubFactory(EventFactory)
    partner = SubFactory(PartnerFactory)


class EventCounterFactory(DjangoModelFactory):
    class Meta:
        model = EventCounter

    event = SubFactory(EventFactory)
    counter = SubFactory(CounterFactory)


class EventPlanItemFactory(DjangoModelFactory):
    class Meta:
        model = EventPlanItem

    title = factory.Faker('sentence')
    event = Iterator(Event.objects.all())
    speaker = Iterator(Speaker.objects.all())
    description = factory.Faker('text', max_nb_chars=200,)


class NewsFactory(DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Faker('text', max_nb_chars=50)
    entry = factory.Faker('text', max_nb_chars=500)
    description = factory.Faker('text', max_nb_chars=1000)


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    iframe_url = factory.Faker('url')


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
