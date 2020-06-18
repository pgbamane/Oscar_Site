from oscar.apps.partner.strategy import *
from oscar.apps.partner.strategy import Structured as CoreStructured
from collections import namedtuple

# A container for policies
PurchaseInfo = namedtuple(
    'PurchaseInfo', ['weight', 'price', 'availability', 'stockrecord', 'pricing_strategy'])


class Structured(CoreStructured):
    def fetch_for_product(self, product, stockrecord=None):
        purchase_info = super(Structured, self).fetch_for_product(product, stockrecord)
        # stockrecord = self. if purchase_info.stockrecord is None
        pricing_strategy = purchase_info.stockrecord.pricing_strategy if purchase_info.stockrecord is not None else None
        return PurchaseInfo(
            price=purchase_info.price,
            availability=purchase_info.availability,
            stockrecord=purchase_info.stockrecord,
            pricing_strategy=pricing_strategy,
            weight=None,
        )

    def fetch_weight_for_parent(self, product):
        children_stock = self.select_children_stockrecords(product)
        # first variant weight is the parent weight
        first_child = children_stock[0][0]
        parent_weight_with_unit = "{} {}".format(first_child.weight, first_child.weight_unit)
        return parent_weight_with_unit

    def fetch_for_parent(self, product):
        purchase_info = super(Structured, self).fetch_for_parent(product)
        # pricing_strategy = children_stock[0][1]
        return PurchaseInfo(
            weight=self.fetch_weight_for_parent(product),
            price=purchase_info.price,
            availability=purchase_info.availability,
            stockrecord=purchase_info.stockrecord,
            pricing_strategy=self.parent_price_pricing_strategy(product),
        )

    def parent_price_pricing_strategy(self, product):
        # select child stock records for parent product() its a tuple of product and stockrecord
        children_stock = self.select_children_stockrecords(product)
        #         select first child stock record pricing strategy as prices and availability are also of first child
        if children_stock:
            pricing_strategy = (children_stock[0][1].pricing_strategy if children_stock[0][1] else None)
            return pricing_strategy

        return None


# class NoTax(CoreNoTax):
#     def parent_pricing_policy(self, product, children_stock):
#         FixedPrice = super(NoTax, self).parent_pricing_policy(product, children_stock)


class Default(UseFirstStockRecord, StockRequired, NoTax, Structured):
    """
        Default stock/price strategy that uses the first found stockrecord for a
        product, ensures that stock is available (unless the product class
        indicates that we don't need to track stock) and charges zero tax.
        """


class Selector(object):
    """
    Responsible for returning the appropriate strategy class for a given
    customer_final/session.

    This can be called in three ways:

    #) Passing a request and customer_final.  This is for determining
       prices/availability for a normal customer_final browsing the site.

    #) Passing just the customer_final.  This is for offline processes that don't
       have a request instance but do know which customer_final to determine prices for.

    #) Passing nothing.  This is for offline processes that don't
       correspond to a specific customer_final.  Eg, determining a price to store in
       a search index.

    """

    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instanticated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return Default(request)
