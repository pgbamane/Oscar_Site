# from oscar.apps.catalogue.models import *  # noqa isort:skip
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):
    # product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, default='')


from oscar.apps.catalogue.models import *
