from django.urls import path

from apps.events.views import (
    BlogDetailView,
    BlogView,
    HomeView,
    PrivacyPolicyView,
    RegistrationCreateView,
    RegistrationDetailView,
    RegistrationSuccessTemplateView,
    RegulationsView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration_create/', RegistrationCreateView.as_view(), name='registration_create'),
    path('registration/<str:unique_code>/', RegistrationDetailView.as_view(), name='registration_detail'),
    path('registration_success/', RegistrationSuccessTemplateView.as_view(), name='registration_success'),
    path('regulations/', RegulationsView.as_view(), name='regulations'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/', BlogView.as_view(), name='blog'),
]
