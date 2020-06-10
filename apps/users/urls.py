from django.urls import path, include
from apps.customer import views
from apps.customer.forms.socialaccount_forms import SignupForm
# # from allauth.socialaccount.views import S
from allauth.account.views import LoginView, AccountInactiveView, LogoutView
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.views import SignupView

urlpatterns = \
    [
        # all-auth urls: first matching url will be called
        path('accounts/signup/', views.SignupView.as_view(), name="account_signup"),
        path('accounts/login/', LoginView.as_view(), name="account_login"),
        path('accounts/logout/', LogoutView.as_view(
            template_name="account/logout.html"),
             name="account_logout"),
        path('accounts/inactive/', AccountInactiveView.as_view(), name="account_inactive"),
        path('accounts/socialaccount_signup/',
             SignupView.as_view(form_class=SignupForm),
             name='socialaccount_signup'),
        path('accounts/', include(default_urlpatterns(GoogleProvider))),
        path('accounts/', include('allauth.urls')),
    ]
