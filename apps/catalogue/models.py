# from oscar.apps.catalogue.models import *  # noqa isort:skip
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct
# from ..catalogue.managers import MyProductManager, MyBrowsableProductManager
from django.utils.functional import cached_property
from oscar.core.loading import get_model

WEIGHT_UNIT_CHOICES = (
    ('kilogram', 'Kg'),
    ('litre', 'Ltr'),
    ('millilitre', 'ML')
    # ('none', None),
)


class Product(AbstractProduct):
    # id = models.AutoField(primary_key=True, )
    # product_name = models.CharField(max_length=50, default='')

    # quantity_per_unit = models.IntegerField(blank=True,
    #                                         null=True,
    #                                         help_text=_(
    #                                                 'quantity that items are shipped per unit. Ex. 1Ltr per bottle of oil'))
    # unit_price = models.FloatField(blank=True,
    #                                null=True,
    #                                help_text=_('Price per unit of product. Ex. Price of 1Ltr oil per bottle'))

    weight_unit = models.CharField(max_length=20,
                                   choices=WEIGHT_UNIT_CHOICES,
                                   default='',
                                   help_text=_(
                                       'Unit used to measure Weight. Ex. Kilogram used to measure quanitity of Pulses. '
                                       'Optional for child product. For parent specify it.'))

    weight = models.IntegerField(help_text=_('Total weight of this Product Purchase'), null=True, blank=True)
    # total_price = models.FloatField(help_text=_('Total price of this Product Purchase'), null=True, blank=True)

    # is_active = models.BooleanField(default=True,
    #                                 help_text=_("Is it ready to sale or not ?."))
    tag = models.CharField(max_length=100,
                           default='',
                           blank=True,
                           help_text=_('Specify tag for child product only. Ex. Certified Organic'))

    # objects = MyProductManager()
    # browsable = MyBrowsableProductManager()

    @cached_property
    def offers(self):
        """
            It returns all types of offers available for this product
        """
        RangeProduct = get_model('offer', 'RangeProduct')
        ConditionalOffer = get_model('offer', 'ConditionalOffer')
        Condition = get_model('offer', 'Condition')

        product_ranges = RangeProduct.objects.select_related('range')
        print(product_ranges.query)
        product_ranges = product_ranges.filter(product=self)

        product_offers = ConditionalOffer.objects.none()
        for product_range in product_ranges:
            condition_ranges = Condition.objects.prefetch_related('offers').filter(range=product_range.range)
            for condition_range in condition_ranges:
                product_offers = product_offers.union(condition_range.offers.all())
            # product_offers =  condition_range.offers.all()

        return product_offers

    @cached_property
    def site_offers(self):
        """
        It returns Site offers avaialable for this product
        :return:
        """
        ConditionalOffer = get_model('offer', 'ConditionalOffer')

        product_offers = self.offers
        site_offers = product_offers.filter(offer_type=ConditionalOffer.SITE)
        return site_offers


from oscar.apps.catalogue.models import *
