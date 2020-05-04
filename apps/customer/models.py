# # from oscar.apps.customer.models import *  # noqa isort:skip
# from oscar.apps.customer.abstract_models import AbstractUser
# from django.db import models
# from django.utils.translation import ugettext_lazy as _
#
# GENDER_OPTIONS = [
#     ('female', 'Female'),
#     ('male', 'Male')
# ]
#
#
# class User(AbstractUser):
#     gender = models.CharField(max_length=20, choices=GENDER_OPTIONS, blank=True, default="")
#     address = models.CharField(max_length=255, help_text="Flat No, Building, Street, Area", default="")
#     locality = models.CharField(max_length=50, help_text='Locality/Town', default="")
#     state = models.CharField(max_length=50, default="")
#     district = models.CharField(max_length=50, default="")
#     city = models.CharField(max_length=50, help_text="City or Taluka", default="")
#     pincode = models.CharField(max_length=10, help_text="Pincode stored as Chars", default="")
#
#     phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True
#                                     )  # unique treats null=True different values, but empty string will not be unique
#
#     REQUIRED_FIELDS = ['phone_number']
#
#     is_superuser = models.BooleanField(
#         _('is_superuser'),
#         db_column='Is Superuser',
#         default=False,
#         help_text=_(
#             'Designates whether this user has all permissions in the admin page or not'
#         )
#     )
#
#     class Meta:
#         # db_table = 'auth_user'
#         swappable = 'AUTH_USER_MODEL'
#
#     def __str__(self):
#         "return email_id of user"
#         return self.get_username()
#
#     @property
#     def is_active_user(self):
#         "Is the user active?"
#         return self.is_active
#
#     @property
#     def is_staff_user(self):
#         "Is user is member of staff?"
#         return self.is_staff
#
#     @property
#     def is_super_user(self):
#         "Is the user a superuser?"
#         return self.is_superuser
#
#     # access of the user to admin content: permissions
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         if self.is_staff or self.is_superuser:
#             return True
#         else:
#             return False
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#
# from oscar.apps.customer.models import *
