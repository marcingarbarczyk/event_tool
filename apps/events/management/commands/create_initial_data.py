from django.core.management.base import BaseCommand, CommandError
from apps.events.factories import (  # replace YOUR_APP_NAME with your app name
    SpeakerFactory, BundleFactory, CounterFactory, EventSpeakerFactory,
    EventBundleFactory, EventBundlePriceFactory, EventBundleCodeDiscountFactory,
    EventPartnerFactory, EventCounterFactory, EventFactory, EventPlanItemFactory,
    NewsFactory, PhotoFactory,
    VideoFactory, RegistrationFactory
)
from apps.events.models import Speaker, News, Counter, Event


class Command(BaseCommand):
    help = 'Creates some initial data for the app.'

    def handle(self, *args, **options):
        Speaker.objects.all().delete()
        News.objects.all().delete()
        Counter.objects.all().delete()
        Event.objects.all().delete()

        for _ in range(25):
            SpeakerFactory.create()
            NewsFactory.create()

        for _ in range(2):
            BundleFactory.create()

        for _ in range(4):
            CounterFactory.create()

        EventFactory.create()

        for _ in range(5):
            EventSpeakerFactory.create()

        for _ in range(10):
            EventPlanItemFactory.create()



        # for _ in range(3):
        #     EventSpeakerFactory.create()
        #     EventBundleFactory.create()
        #     EventPartnerFactory.create()
        #     EventCounterFactory.create()
        #
        # EventBundlePriceFactory.create()
        # EventBundleCodeDiscountFactory.create()
        # EventPlanItemFactory.create()
        #
        # PhotoFactory.create()
        # VideoFactory.create()
        # RegistrationFactory.create()

        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))
