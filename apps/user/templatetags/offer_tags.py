# from django import template
# from apps.offer.models import RangeProduct, Condition, ConditionalOffer
#
# register = template.Library()
#
#
# @register.simple_tag
# def offers_for_product(request, product):
#     product_ranges = RangeProduct.objects.select_related('range')
#     print(product_ranges.query)
#     product_ranges = product_ranges.filter(product=product)
#
#     product_offers = ConditionalOffer.objects.none()
#     for product_range in product_ranges:
#         condition_ranges = Condition.objects.prefetch_related('offers').filter(range=product_range.range)
#         for condition_range in condition_ranges:
#             product_offers = product_offers.union(condition_range.offers.all())
#         # product_offers =  condition_range.offers.all()
#
#     return product_offers
#
#
# @register.simple_tag
# def site_offers_for_product(request, product):
#     product_offers = offers_for_product(request, product)
#     site_offers = product_offers.filter(offer_type=ConditionalOffer.SITE)
#     return site_offers
