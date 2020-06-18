from .. import strategy
from django.test import TestCase
from oscar.test import factories
from oscar.core.loading import get_model, get_class

Product = get_model('catalogue', 'Product')
Unavailable = get_class('partner.availability', 'Unavailable')
Available = get_class('partner.availability', 'Available')


class TestDefaultStrategy(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.parent_product = factories.create_product(title=u"Almond Oil",
                                                      product_class=u"Oils")
        cls.child_product = factories.create_product(title=u"Almond Oil 2Ltr",
                                                     structure=Product.CHILD,
                                                     parent=cls.parent_product,
                                                     product_class=u"Oils")

    def setUp(self):
        self.strategy = strategy.Default()

    def test_no_stockrecords_for_parent(self):
        ""

    def test_no_stockrecords_for_child(self):
        """
        test child product which has no stockrecords
        """
        info = self.strategy.fetch_for_product(self.child_product)
        # self.assertEqual(info.price, Unavailable({}))
        self.assertFalse(info.availability.is_available_to_buy)
        self.assertIsNone(info.stockrecord)
        self.assertIsNone(info.pricing_strategy)
        self.assertIsNone(info.weight)
