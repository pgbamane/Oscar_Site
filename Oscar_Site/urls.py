from django.conf.urls import url
from oscar.app import application
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    path('admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),

    path('', application.urls),
]
