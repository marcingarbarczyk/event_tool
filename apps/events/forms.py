from django import forms

from apps.dynamoforms.forms import DynamoForm
from apps.events.models import EventBundleCodeDiscount


class BundleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.bundle.name}'


class RegistrationForm(DynamoForm):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        if self.event is not None:
            kwargs['form_id'] = self.event.form.id
            super().__init__(*args, **kwargs)
            self.fields['selected_bundle'].queryset = self.event.active_bundles
            self.fields['agreement'].label = self.event.privacy_policy_checkbox
        else:
            raise ValueError('No event provided for the registration form.')

    name = forms.CharField(
        required=True,
        label='Imię i nazwisko *',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label='Email *',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    phone = forms.CharField(
        required=True,
        label='Telefon *',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    selected_bundle = BundleChoiceField(
        required=True,
        queryset=None,
        label='Wybrany pakiet *',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    agreement = forms.BooleanField(
        required=True,
        label='',
    )


class PaymentForm(forms.Form):
    def __init__(self, registration, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.registration = registration
        self.discount_codes = registration.selected_bundle.active_discounts
        self.selected_code_discount = None
        if not self.discount_codes or self.registration.selected_code_discount:
            self.fields.pop('discount_code')

    discount_code = forms.CharField(
        max_length=50,
        required=False,
        label='Kod rabatowy',
    )

    def clean_discount_code(self):
        discount_code = self.cleaned_data['discount_code']
        if discount_code:
            try:
                self.selected_code_discount = self.discount_codes.get(code__iexact=discount_code)
            except EventBundleCodeDiscount.DoesNotExist:
                raise forms.ValidationError('Nieprawidłowy kod rabatowy.')
        return discount_code
