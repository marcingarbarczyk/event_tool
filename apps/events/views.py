from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.dynamo_forms.models import Answer, Field, UserAnswers
from apps.events.forms import PaymentForm, RegistrationForm
from apps.events.models import Event, News, Photo, Registration, Video
from utils.tpay import get_tpay_url


class HomeView(TemplateView):
    """
    Main view for the events' app.
    """

    template_name = 'events/home.html'

    def get_template_names(self):
        event = self.get_event()
        return ['events/event_required.html'] if not event else super().get_template_names()

    def get_event(self):
        if not hasattr(self, '_event'):
            self._event = Event.current()
        return self._event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_event()
        if event:
            context['event'] = event
            context['news'] = News.objects.all().order_by('-date')[0:3]
            context['photos'] = Photo.objects.all().order_by('order')
            context['videos'] = Video.objects.all().order_by('order')
            if event.form:
                context['registration_form'] = RegistrationForm(event=event)
        return context


class RegulationsView(TemplateView):
    """
    View for regulations.
    """

    template_name = 'events/regulations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regulations'] = Event.current().regulations
        return context


class PrivacyPolicyView(TemplateView):
    """
    View for privacy policy.
    """

    template_name = 'events/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy_policy'] = Event.current().privacy_policy
        return context


class BlogView(ListView):
    """
    View for blog.
    """

    template_name = 'events/blog.html'
    model = News
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.current()
        return context


class BlogDetailView(DetailView):
    """
    View for blog detail.
    """

    model = News
    template_name = 'events/blog_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.current()
        return context


class RegistrationDetailView(DetailView):
    """
    View for registration detail.
    """

    model = Registration
    template_name = 'events/payment.html'
    context_object_name = 'registration'
    slug_field = 'unique_code'
    slug_url_kwarg = 'unique_code'

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registration = self.object

        if registration.selected_bundle:
            context['price'] = registration.final_price
            context['form'] = (
                kwargs['form']
                if 'form' in kwargs and kwargs['form'] is not None
                else PaymentForm(registration=context['registration'])
            )
        return context

    def get_result_url(self, request):
        if settings.DEBUG:
            return settings.TPAY_DEBUG_RESULT_URL
        else:
            return request.build_absolute_uri(reverse('tpay_payment'))

    def get_return_url(self, request):
        if settings.DEBUG:
            return settings.TPAY_DEBUG_RETURN_URL
        else:
            return request.build_absolute_uri(reverse('registration_success'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # pierwsze zamówienia nie miały pakietów
        # niestety informacja stracona
        if not self.object.selected_bundle:
            return HttpResponseNotAllowed(['POST'])

        form = PaymentForm(registration=self.object, data=request.POST)
        if form.is_valid() and not self.object.is_paid:
            unique_code = self.object.unique_code
            date_start = datetime.strftime(self.object.event.date_start, '%Y-%m-%d')
            discount_code = form.selected_code_discount
            if discount_code:
                self.object.selected_code_discount = discount_code
                self.object.save()
            total_cost = self.object.final_price
            order_description = f'{self.object.event.name} - {date_start}'
            result_url = self.get_result_url(request)
            return_url = self.get_return_url(request)
            tpay_link = get_tpay_url(
                total_cost=total_cost,
                order_description=order_description,
                crc=unique_code,
                shipping_name=self.object.name,
                shipping_email=self.object.email,
                result_url=result_url,
                return_url=return_url,
            )
            return redirect(tpay_link)
        kwargs['form'] = form
        return self.render_to_response(self.get_context_data(**kwargs))


class RegistrationSuccessTemplateView(TemplateView):
    """
    View for registration success.
    """

    template_name = 'events/registration_success.html'


class RegistrationCreateView(View):
    def post(self, request, *args, **kwargs):
        event = Event.current()
        form = RegistrationForm(request.POST, event=event)
        if form.is_valid():
            user_answers = UserAnswers.objects.create()
            self._process_form_answers(form, user_answers)
            registration = self._create_registration(form, user_answers)
            return redirect('registration_detail', unique_code=registration.unique_code)
        else:
            return HttpResponse(_('Failed to submit the form. Please try again later.'))

    def _process_form_answers(self, form, user_answers):
        dynamo_form = form.event.form
        answers_to_create = []
        for section in dynamo_form.sections.filter(is_active=True):
            for field in section.fields.filter(is_active=True):
                if field.name not in form.ignore_fields:
                    answer = form.cleaned_data[field.name]
                    if field.field_type == Field.RADIO:
                        answer = field.choices.all().get(id=answer).choice

                    answers_to_create.append(
                        Answer(
                            field=field,
                            answer=answer,
                            user_answers=user_answers,
                        )
                    )
        Answer.objects.bulk_create(answers_to_create)

    def _create_registration(self, form, user_answers):
        data = form.cleaned_data
        return Registration.objects.create(
            email=data['email'],
            name=data['name'],
            phone=data['phone'],
            user_answers=user_answers,
            selected_bundle=data['selected_bundle'],
            event=form.event,
        )
