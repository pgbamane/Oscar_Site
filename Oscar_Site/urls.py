from django.conf.urls import url
from oscar.app import application
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LoginView, AccountInactiveView, LogoutView

from apps.customer_final import views
# from allauth.socialaccount.views import S
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.views import SignupView

urlpatterns = \
    [
        # The Django admin is not officially supported; expect breakage.
        # Nonetheless, it's often useful for debugging.
        path('admin/', admin.site.urls),

        path('i18n/', include('django.conf.urls.i18n')),

        # users app urls
        path('', include('apps.users.urls')),

        # oscar urls
        path('', application.urls),

        # all-auth urls
        # path('auth_accounts/signup/', views.SignupView.as_view(), name="account_signup"),
        # path('auth_accounts/login/', LoginView.as_view(), name="account_login"),
        # path('auth_accounts/logout/', LogoutView.as_view(
        #     template_name="account/logout.html"),
        #      name="account_logout"),
        # path('accounts/inactive', AccountInactiveView.as_view(), name="account_inactive"),
        # path('accounts/socialaccount_signup', SignupView.as_view(), name='socialaccount_signup'),
        # # # path('accounts/socialaccount_signup', SignupView.as_view(), name='socialaccount_signup'),
        # path('accounts/', include(default_urlpatterns(GoogleProvider))),
        # path('accounts/', include('allauth.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
