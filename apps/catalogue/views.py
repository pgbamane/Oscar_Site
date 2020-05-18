from django.shortcuts import render
from oscar.apps.catalogue.views import *
from django.views.generic import View
from oscar.core.loading import get_model


# def update_product_info(request, *args, product_id):
#     print("Product Id:", product_id)
#     return render(request, 'catalogue/partials/product_info.html')

class ProductInfo(View):
    Product = get_model('catalogue', 'Product')

    def get(self, request, *args, **kwargs):
        # print("Product Id:", product_id)
        product_id = kwargs.get('product_id', None)
        product = Product.objects.get(pk=product_id)
        # super(ProductInfo, self).get(request, *args, **kwargs)
        return render(request, 'catalogue/partials/product_info.html', {'product': product})
