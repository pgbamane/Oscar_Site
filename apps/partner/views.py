from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from oscar.apps.partner.views import *
from django.views.generic import TemplateView
from oscar.core.loading import get_model
from oscar.apps.partner.views import *


class StockRecord(TemplateView):
    model = get_model('catalogue', 'Product')
    queryset = model.objects.all()
    template_name = 'catalogue/partials/stock_record.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get('pk', None)
        if product_id:
            try:
                context['product'] = self.queryset.get(pk=product_id)
            except ObjectDoesNotExist:
                HttpResponse('Product does not exist')
        return context
