from oscar.apps.partner.abstract_models import AbstractStockRecord
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StockRecord(AbstractStockRecord):
    PREMIUM, GOLD, EMPTY = 'Premium', 'Gold', 'None'
    PRICING_OPTIONS = (
        (PREMIUM, 'Premium'),
        (GOLD, 'Gold'),
        (EMPTY, 'None'),
    )

    pricing_strategy = models.CharField(max_length=100,
                                        default=EMPTY,
                                        choices=PRICING_OPTIONS,
                                        blank=True,
                                        help_text=_(
                                            "Specify Premium or Gold for child products. Not neccessary for Parent"))


from oscar.apps.partner.models import *  # noqa isort:skip
