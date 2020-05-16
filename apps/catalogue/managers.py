# from oscar.apps.catalogue.managers import ProductQuerySet as BaseQuerySet
#
# # class ProductQuerySet(BaseQuerySet):
# #
# #     def browsable(self):
# #         """
# #         Only child products.
# #         """
# #         return self.filter(title__startswith='Ground')
# #
#
# from oscar.apps.catalogue.managers import (ProductManager as CoreProductManager,
#                                            BrowsableProductManager as CoreBrowsableProductManager)
#
# 
# class ProductMyQuerySet(BaseQuerySet):
#
#     def browsable(self):
#         """
#         Only child products.
#         """
#         print("Callllllllllllllllllled")
#         # return self.filter(title__startswith='Ground')
#
#
# class MyProductManager(CoreProductManager):
#     def get_queryset(self):
#         return ProductMyQuerySet(self.model, using=self._db)
#
#
# class MyBrowsableProductManager(CoreBrowsableProductManager):
#     pass
