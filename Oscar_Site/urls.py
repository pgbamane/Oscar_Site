from django.conf.urls import url
from oscar.app import application
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = \
    [
        # The Django admin is not officially supported; expect breakage.
        # Nonetheless, it's often useful for debugging.
        path('admin/', admin.site.urls),

        path('i18n/', include('django.conf.urls.i18n')),

        # oscar urls
        path('', application.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
