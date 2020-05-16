# from oscar.apps.catalogue.models import *  # noqa isort:skip
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct
# from ..catalogue.managers import MyProductManager, MyBrowsableProductManager

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


from oscar.apps.catalogue.models import *
