from django import template
from oscar.core.loading import get_model

register = template.Library()


@register.simple_tag
def sale_price_for_product(request, product, benefit_value):
    if product.is_parent:
        purchase_info = request.strategy.fetch_for_parent(product)
    else:
        purchase_info = request.strategy.fetch_for_product(product)
    # StockRecord = get_model('Partner', 'StockRecord')

    product_price = purchase_info.price.excl_tax
    discount = product_price * (benefit_value / 100)
    sale_price = product_price - discount
    return sale_price
