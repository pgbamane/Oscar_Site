from django.shortcuts import render
from oscar.apps.catalogue.views import *
from django.views.generic import TemplateView
from oscar.core.loading import get_model


# class ProductInfo(View):
#     Product = get_model('catalogue', 'Product')
#
#     def get(self, request, *args, **kwargs):
#         # print("Product Id:", product_id)
#         product_id = kwargs.get('product_id', None)
#         product = Product.objects.get(pk=product_id)
#         # super(ProductInfo, self).get(request, *args, **kwargs)
#         return render(request, 'catalogue/partials/product_info.html', {'product': product})

class ProductInfo(DetailView):
    model = get_model('catalogue', 'Product')
    queryset = model.objects.all()
    template_name = 'catalogue/partials/product_info.html'
    context_object_name = 'product'


class PriceDetails(TemplateView):
    template_name = 'catalogue/partials/price_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get('pk', None)
        Product = get_model('catalogue', 'Product')
        # context['product'] = None
        if product_id:
            try:
                context['product'] = Product.objects.get(pk=product_id)
                return context
            except Product.DoesNotExist:
                # return HttpResponse('Product does not exist')
                return context
