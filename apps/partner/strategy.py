from oscar.apps.partner.strategy import *
from oscar.apps.partner.strategy import Structured as CoreStructured
from collections import namedtuple

# A container for policies
PurchaseInfo = namedtuple(
    'PurchaseInfo', ['price', 'availability', 'stockrecord', 'pricing_strategy'])


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
        )

    def fetch_for_parent(self, product):
        purchase_info = super(Structured, self).fetch_for_parent(product)
        # pricing_strategy = children_stock[0][1]
        return PurchaseInfo(
            price=purchase_info.price,
            availability=purchase_info.availability,
            stockrecord=purchase_info.stockrecord,
            pricing_strategy=self.parent_price_pricing_strategy(product),
        )

    def parent_price_pricing_strategy(self, product):
        # select child stock records for parent product() its a tuple of product and stockrecord
        children_stock = self.select_children_stockrecords(product)
        #         select first child stock record pricing strategy as prices and availability are also of first child
        pricing_strategy = children_stock[0][1].pricing_strategy
        return pricing_strategy


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
    user/session.

    This can be called in three ways:

    #) Passing a request and user.  This is for determining
       prices/availability for a normal user browsing the site.

    #) Passing just the user.  This is for offline processes that don't
       have a request instance but do know which user to determine prices for.

    #) Passing nothing.  This is for offline processes that don't
       correspond to a specific user.  Eg, determining a price to store in
       a search index.

    """

    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instanticated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return Default(request)
