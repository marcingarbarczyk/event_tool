from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.dynamo_forms.models import Form, UserAnswers
from apps.events.utils import generate_unique_code
from apps.script_manager.models import Script
from utils.mail import send_message_via_email
from utils.models import ActiveMixin, Orderable, SocialMediaMixin


class Speaker(SocialMediaMixin):
    """
    The `Speaker` class represents a speaker at a conference.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_('full name'),
    )
    description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    image = models.ImageField(
        upload_to='speakers/',
        null=True,
        blank=True,
        verbose_name=_('photo'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('speakers')
        verbose_name = _('speaker')


class Counter(models.Model):
    """
    A class representing a counter.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
    )
    value = models.IntegerField(
        default=0,
        verbose_name=_('value'),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('counters')
        verbose_name = _('counter')


class Partner(models.Model):
    """
    A class representing a partner.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    image = models.ImageField(
        upload_to='partners/',
        null=True,
        blank=True,
        verbose_name=_('image'),
    )
    url = models.URLField(
        verbose_name=_('link'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('partners')
        verbose_name = _('partner')


class EventSpeaker(Orderable):
    """
    A class representing an order of speakers in an event.
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('event'),
        related_name='event_speakers',
    )
    speaker = models.ForeignKey(
        'Speaker',
        on_delete=models.CASCADE,
        verbose_name=_('speaker'),
    )

    class Meta(Orderable.Meta):
        verbose_name_plural = _('event speakers')
        verbose_name = _('event speaker')


class EventBundle(Orderable, ActiveMixin):
    """
    A class representing an event bundle in an event
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('event'),
        related_name='event_bundles',
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('is featured'),
    )
    is_sold_out = models.BooleanField(
        default=False,
        verbose_name=_('is sold out'),
    )

    @property
    def active_price(self):
        now = timezone.now()
        price = self.prices.filter(is_active=True, activity_range__contains=now).first()
        return price

    @property
    def active_discounts(self):
        return self.discounts.all().filter(is_active=True)

    def __str__(self):
        return f'#{self.event_id} {self.name}'

    class Meta(Orderable.Meta):
        verbose_name_plural = _('event bundles')
        verbose_name = _('event bundle')


class EventBundlePrice(Orderable, ActiveMixin):
    """
    A class representing a cost.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
    )
    price = models.DecimalField(
        default=0,
        verbose_name=_('price'),
        max_digits=7,
        decimal_places=2,
    )
    event_bundle = models.ForeignKey(
        EventBundle,
        related_name='prices',
        on_delete=models.CASCADE,
        verbose_name=_('event bundle'),
    )
    activity_range = DateRangeField(
        verbose_name=_('valid dates'),
    )

    class Meta(Orderable.Meta):
        verbose_name_plural = _('bundle costs')
        verbose_name = _('bundle cost')


class EventBundleCodeDiscount(ActiveMixin):
    """
    A class to represent a discount in the event bundle
    """

    code = models.CharField(
        max_length=50,
        verbose_name=_('discount code'),
    )
    event_bundle = models.ForeignKey(
        EventBundle, related_name='discounts', on_delete=models.CASCADE, verbose_name=_('event bundle')
    )
    discount = models.DecimalField(
        default=0,
        verbose_name=_('discount value'),
        max_digits=7,
        decimal_places=2,
    )

    def __str__(self):
        return f'{self.event_bundle} - {self.discount}'

    class Meta:
        verbose_name_plural = _('discount codes')
        verbose_name = _('discount code')
        unique_together = (
            'code',
            'event_bundle',
        )


class EventPartner(Orderable):
    """
    A class representing an order of partners in an event.
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('event'),
        related_name='event_partners',
    )
    partner = models.ForeignKey(
        'Partner',
        on_delete=models.CASCADE,
        verbose_name=_('partner'),
    )

    class Meta(Orderable.Meta):
        verbose_name_plural = _('event partners')
        verbose_name = _('event partner')


class EventCounter(Orderable):
    """
    A class representing an order of counters in an event.
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('event'),
        related_name='event_counters',
    )
    counter = models.ForeignKey(
        'Counter',
        on_delete=models.CASCADE,
        verbose_name=_('counter'),
    )

    class Meta(Orderable.Meta):
        verbose_name_plural = _('event counters')
        verbose_name = _('event counter')


class Event(SocialMediaMixin):
    """
    A class representing an event.
    """

    logo = models.ImageField(
        upload_to='logos/',
        null=True,
        blank=True,
        verbose_name=_('logo'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    introduction = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('introduction'),
    )
    description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    partners_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('partners section text'),
    )
    max_registrations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('maximum number of registrations'),
    )
    privacy_policy = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('privacy policy'),
    )
    regulations = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('regulations'),
    )
    privacy_policy_checkbox = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('consent text in form'),
    )
    additional_description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('additional description'),
    )
    date_start = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('start date'),
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('event form'),
    )
    speakers = models.ManyToManyField(
        'Speaker',
        through='EventSpeaker',
        blank=True,
        verbose_name=_('speakers'),
    )
    partners = models.ManyToManyField(
        'Partner',
        through='EventPartner',
        blank=True,
        verbose_name=_('partners'),
    )
    counters = models.ManyToManyField(
        'Counter',
        through='EventCounter',
        blank=True,
        verbose_name=_('counters'),
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('city'),
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('address'),
    )
    place = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('place'),
    )
    background_image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True,
        verbose_name=_('background image'),
    )
    promo_movie_html = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('promotional video iframe'),
    )
    footer_text = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('footer text'),
    )
    google_tag_manager_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('google tag manager id'),
    )

    @staticmethod
    def current():
        return (
            Event.objects.all()
            .select_related(
                'form',
            )
            .prefetch_related(
                'event_bundles',
                'form__sections__fields__choices',
                'form__sections__field_choice__field',
                'event_speakers__speaker',
                'event_partners__partner',
                'event_counters__counter',
                'plan_items__speaker',
            )
            .last()
        )

    @property
    def registrations_remaining_count(self):
        registrations_remaining_count = self.max_registrations - self.registrations.filter(is_paid=True).count()
        return max(0, registrations_remaining_count)

    @property
    def start(self):
        return self.date_start.strftime('%Y/%m/%d')

    @property
    def active_bundles(self):
        return self.event_bundles.filter(is_active=True)

    @property
    def start_month_name(self):
        months = {
            1: _('January'),
            2: _('February'),
            3: _('March'),
            4: _('April'),
            5: _('May'),
            6: _('June'),
            7: _('July'),
            8: _('August'),
            9: _('September'),
            10: _('October'),
            11: _('November'),
            12: _('December'),
        }
        return months[self.date_start.month]

    @property
    def start_month_short_name(self):
        months = {
            1: _('Jan'),
            2: _('Feb'),
            3: _('Mar'),
            4: _('Apr'),
            5: _('May'),
            6: _('Jun'),
            7: _('Jul'),
            8: _('Aug'),
            9: _('Sep'),
            10: _('Oct'),
            11: _('Nov'),
            12: _('Dec'),
        }
        return months[self.date_start.month]

    @property
    def available_places(self):
        available_places = self.registrations_remaining_count - self.registrations.filter(is_paid=True).count()
        return max(0, available_places)

    def __str__(self):
        return f'{self.name} ({self.start})'

    class Meta:
        ordering = ['id']
        verbose_name_plural = _('events')
        verbose_name = _('event')


class EventPlanItem(Orderable):
    """
    A class representing an item in the event plan.
    """

    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
    )
    hours = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('hours'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='plan_items',
        verbose_name=_('event'),
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('speaker'),
    )
    image = models.ImageField(
        upload_to='plan/',
        null=True,
        blank=True,
        verbose_name=_('image'),
    )

    def __str__(self):
        return self.title

    class Meta(Orderable.Meta):
        verbose_name_plural = _('plan items')
        verbose_name = _('plan item')


class News(models.Model):
    """
    A class representing a news.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
    )
    entry = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('entry'),
    )
    description = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    image = models.ImageField(
        upload_to='news/',
        null=True,
        blank=True,
        verbose_name=_('image'),
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('publication date'),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('slug'),
    )

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        if News.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f'{slug}-{self.id}'
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name_plural = _('News')
        verbose_name = _('News')


class Photo(Orderable):
    """
    A class representing a photo in the gallery.
    """

    image = models.ImageField(
        upload_to='photos/',
        verbose_name=_('photo'),
    )

    def __str__(self):
        return self.image.url

    class Meta(Orderable.Meta):
        verbose_name_plural = _('photos')
        verbose_name = _('photo')


class Video(Orderable):
    """
    A class representing a video.
    """

    iframe_url = models.URLField(
        verbose_name=_('iframe URL'),
    )
    is_vertical = models.BooleanField(
        default=False,
        verbose_name=_('vertical'),
    )
    thumbnail = models.ImageField(
        upload_to='videos/',
        verbose_name=_('thumbnail'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta(Orderable.Meta):
        verbose_name_plural = _('videos')
        verbose_name = _('video')


class Registration(models.Model):
    """
    A class representing an event registration.
    """

    email = models.EmailField(
        verbose_name=_('email'),
    )
    phone = models.CharField(
        blank=True,
        max_length=25,
        default='',
        verbose_name=_('phone'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    selected_bundle = models.ForeignKey(
        EventBundle,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('selected bundle'),
    )
    selected_code_discount = models.ForeignKey(
        EventBundleCodeDiscount,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('selected discount code'),
    )
    unique_code = models.CharField(
        max_length=50,
        verbose_name=_('unique code'),
        unique=True,
        default=generate_unique_code,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='registrations',
        verbose_name=_('event'),
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('registration date'),
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('paid'),
    )
    paid_amount = models.DecimalField(
        verbose_name=_('paid amount'),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    tpay_notification = models.JSONField(
        null=True,
        blank=True,
    )
    user_answers = models.ForeignKey(
        UserAnswers,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('customer answers'),
        related_name='registration',
    )

    @property
    def final_price(self):
        final_price = self.selected_bundle.active_price.price
        if self.selected_code_discount:
            final_price = final_price - self.selected_code_discount.discount
        return str(final_price)

    @staticmethod
    def store_responses(data):
        data = data.copy()
        del data['email']
        del data['name']
        del data['form_id']
        formatted_responses = ''
        for _none, value in data.items():
            formatted_responses += f'{value}\n'
        return formatted_responses

    def send_payment_email_notification(self):
        registration_url = (
            f"{settings.BASE_URL}{reverse('registration_detail', kwargs={'unique_code': self.unique_code})}"
        )

        send_message_via_email(
            subject=_('Registration Confirmation'),
            template='events/email/registration.html',
            context={
                'registration': self,
                'url': registration_url,
            },
            to=[self.email],
        )

    def send_new_paid_registration_email_notification(self):
        answers = self.user_answers.answers.order_by('field__section__order', 'field__order')

        send_message_via_email(
            subject=_('New Event Registration Paid'),
            template='events/email/new_paid_registration.html',
            context={'registration': self, 'answers': answers},
            to=settings.NEW_REGISTRATIONS_EMAIL_RECEIVERS,
        )

    def send_successful_payment_email_notification(self):
        send_message_via_email(
            subject=_('Event Access Paid'),
            template='events/email/success_payment.html',
            context={
                'registration': self,
            },
            to=[self.email],
        )

    def __str__(self):
        return f'{self.unique_code} {self.email} ({self.event})'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self.pk is None
        super().save(force_insert, force_update, using, update_fields)
        if is_new:
            self.send_payment_email_notification()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = _('registrations')
        verbose_name = _('registration')


class EventScript(models.Model):
    """
    A class representing a script.
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('event'),
        related_name='event_scripts',
    )
    script = models.ForeignKey(
        Script,
        on_delete=models.CASCADE,
        verbose_name=_('script'),
    )

    def __str__(self):
        return f'{self.event} - {self.script}'

    class Meta:
        verbose_name_plural = _('event scripts')
        verbose_name = _('event script')
