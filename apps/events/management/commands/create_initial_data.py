from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.dynamo_forms.factories import FieldFactory, FormFactory, SectionFactory
from apps.dynamo_forms.models import Answer, Field, FieldChoice, Form, Section
from apps.events.factories import (
    CounterFactory,
    EventBundleFactory,
    EventBundlePriceFactory,
    EventCounterFactory,
    EventFactory,
    EventPlanItemFactory,
    EventSpeakerFactory,
    NewsFactory,
    PartnerFactory,
    PhotoFactory,
    SpeakerFactory,
    SuperUserFactory,
    VideoFactory,
)
from apps.events.models import Counter, Event, News, Photo, Speaker, Video

User = get_user_model()
MODELS = [User, Speaker, News, Counter, Event, Video, Photo, Answer, FieldChoice, Field, Section, Form]


class Command(BaseCommand):
    def handle(self, *args, **options):

        for model in MODELS:
            model.objects.all().delete()

        SuperUserFactory(username='dev', password='123456')  # noqa S106

        FormFactory.create()
        for _ in range(4):
            section = SectionFactory.create()

            for _ in range(3):
                FieldFactory.create(section=section)

        EventFactory.create()

        for _ in range(25):
            SpeakerFactory.create()
        for _ in range(25):
            NewsFactory.create()
        for _ in range(4):
            CounterFactory.create()
        for _ in range(15):
            PartnerFactory.create()
        for _ in range(16):
            PhotoFactory.create()
        for _ in range(8):
            VideoFactory.create()
        for _ in range(8):
            EventPlanItemFactory.create()
        for _ in range(4):
            EventCounterFactory.create()
        for _ in range(5):
            EventSpeakerFactory.create()
        for _ in range(10):
            EventPlanItemFactory.create()
        for _ in range(2):
            EventBundleFactory.create()
        for _ in range(2):
            EventBundlePriceFactory.create()
