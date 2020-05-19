from django.conf.urls import url
from oscar.apps.catalogue.app import CatalogueApplication as CoreCatalogueApplication
# from .views import P


from oscar.core.loading import get_class


class CatalogueApplication(CoreCatalogueApplication):
    product_info_view = get_class('catalogue.views', 'ProductInfo')

    def get_urls(self):
        urlpatterns = super(CatalogueApplication, self).get_urls()
        urlpatterns += [
            url(r'^product_info/(?P<pk>[\d]+)/$', self.product_info_view.as_view(), name='product_info'),
        ]
        return self.post_process_urls(urlpatterns)
        # return urlpatterns


application = CatalogueApplication()
