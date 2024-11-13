from django.contrib import admin

from .models import (
    Counter,
    Event,
    EventBundle,
    EventBundleCodeDiscount,
    EventBundlePrice,
    EventCounter,
    EventPartner,
    EventPlanItem,
    EventScript,
    EventSpeaker,
    News,
    Partner,
    Photo,
    Registration,
    Speaker,
    Video,
)


class EventSpeakerInline(admin.TabularInline):
    model = EventSpeaker
    extra = 1


class EventPartnerInline(admin.TabularInline):
    model = EventPartner
    extra = 1


class EventPlanItemInline(admin.TabularInline):
    model = EventPlanItem
    extra = 1


class EventCounterInline(admin.TabularInline):
    model = EventCounter
    extra = 1


class EventBundlePriceInline(admin.TabularInline):
    model = EventBundlePrice
    extra = 1


class EventBundleInline(admin.TabularInline):
    model = EventBundle
    extra = 1


class EventBundleCodeDiscountInline(admin.TabularInline):
    model = EventBundleCodeDiscount
    extra = 1


class EventScriptInline(admin.TabularInline):
    model = EventScript
    extra = 1


@admin.register(EventBundle)
class EventBundleAdmin(admin.ModelAdmin):
    list_display = [
        'event',
        'is_active',
    ]
    list_filter = [
        'event',
        'is_active',
    ]
    inlines = [
        EventBundlePriceInline,
        EventBundleCodeDiscountInline,
    ]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    search_fields = [
        'name',
    ]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    search_fields = [
        'name',
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'date_start',
    ]
    search_fields = [
        'name',
    ]
    inlines = (
        EventCounterInline,
        EventPartnerInline,
        EventPlanItemInline,
        EventBundleInline,
        EventSpeakerInline,
        EventScriptInline,
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'date',
    ]
    search_fields = [
        'title',
    ]


@admin.register(EventPlanItem)
class EventPlanItemAdmin(admin.ModelAdmin):
    list_display = [
        'event',
        'hours',
        'speaker',
        'title',
    ]
    search_fields = [
        'title',
        'speaker__name',
    ]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'image',
    ]
    search_fields = [
        'image',
    ]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'iframe_url',
    ]


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'value',
    ]
    search_fields = [
        'title',
        'value',
    ]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    actions = [
        'send_confirmation_email',
        'send_successful_payment_email_notification_to_user',
    ]
    list_display = [
        'date',
        'email',
        'name',
        'event',
        'is_paid',
        'paid_amount',
        'unique_code',
        'selected_code_discount',
        'selected_bundle',
    ]
    list_filter = [
        'event__name',
        'selected_bundle',
        'selected_code_discount',
        'is_paid',
    ]
    search_fields = [
        'email',
        'unique_code',
        'name',
    ]
    readonly_fields = [
        'selected_code_discount',
        'email',
        'phone',
        'name',
        'date',
        'email',
        'event',
        'is_paid',
        'selected_bundle',
        'user_answers',
        'paid_amount',
        'tpay_notification',
        'unique_code',
    ]

    def send_successful_payment_email_notification_to_user(self, request, queryset):
        for registration in queryset:
            registration.send_successful_payment_email_notification()

    send_successful_payment_email_notification_to_user.short_description = (
        'Wyślij e-mail o opłaconej konferencji do klienta'
    )

    def send_confirmation_email(self, request, queryset):
        for registration in queryset:
            registration.send_new_paid_registration_email_notification()

    send_confirmation_email.short_description = 'Wyślij e-mail o opłaconej konferencji'


@admin.register(EventBundleCodeDiscount)
class EventBundleCodeDiscountAdmin(admin.ModelAdmin):
    list_filter = [
        'event_bundle',
    ]
    list_display = [
        'code',
        'discount',
        'event_bundle',
    ]
