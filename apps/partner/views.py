from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from oscar.apps.partner.views import *
from django.views.generic import TemplateView
from oscar.core.loading import get_model
from oscar.apps.partner.views import *


class StockRecord(TemplateView):
    template_name = 'catalogue/partials/stock_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get('pk', None)
        Product = get_model('catalogue', 'Product')
        # context['product'] = None
        if product_id:
            try:
                context['product'] = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                # return HttpResponse('Product does not exist')
                return context
        return context
