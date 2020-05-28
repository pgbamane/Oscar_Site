from django.conf.urls import url
from oscar.apps.catalogue.app import CatalogueApplication as CoreCatalogueApplication
# from ..partner import views as partner_
# from .views import P


from oscar.core.loading import get_class


class CatalogueApplication(CoreCatalogueApplication):
    product_info_view = get_class('catalogue.views', 'ProductInfo')
    price_details_view = get_class('catalogue.views', 'PriceDetails')

    def get_urls(self):
        urlpatterns = super(CatalogueApplication, self).get_urls()
        urlpatterns += [
            url(r'^product_info/(?P<pk>[\d]+)/$', self.product_info_view.as_view(), name='product_info'),
            url(r'^price_details/(?P<pk>[\d]+)/$', self.price_details_view.as_view(), name='price_details'),
        ]
        return self.post_process_urls(urlpatterns)
        # return urlpatterns


application = CatalogueApplication()
