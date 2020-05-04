# # from django.contrib.auth.base_user import
# from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
# from django.db import models
# from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _
#
# from customer.managers.user_managers import UserManager
#
# GENDER_OPTIONS = [
#     ('female', 'Female'),
#     ('male', 'Male')
# ]
#
#
# class MyUser():
#     first_name = "Pra"
#
#     def user_save(self, user):
#         user.first_name = self.first_name
#         user.save()
#
#
# class User(PermissionsMixin, AbstractBaseUser):
#     """Django's permission framework gives you all the methods and db fields to support permission model"""
#     first_name = models.CharField(db_column="first_name", max_length=15)
#     last_name = models.CharField(max_length=30)
#     gender = models.CharField(max_length=10, choices=GENDER_OPTIONS, blank=True, default="")
#     address = models.CharField(max_length=255, help_text="Flat No, Building, Street, Area", default="")
#     locality = models.CharField(max_length=20, help_text='Locality/Town', default="")
#     state = models.CharField(max_length=30, default="")
#     district = models.CharField(max_length=30, default="")
#     city = models.CharField(max_length=30, help_text="City or Taluka", default="")
#     pincode = models.CharField(max_length=10, help_text="Pincode stored as Chars", default="")
#
#     phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True
#                                     )  # unique treats null=True different values, but empty string will not be unique
#
#     # primary key of user
#     email = models.EmailField(max_length=40, unique=True, primary_key=True)
#
#     password = models.CharField(max_length=200, default="")
#     date_joined = models.DateTimeField(auto_now_add=True, null=True)
#
#     USERNAME_FIELD = 'email'
#     # no need as email_id is usernamefield
#     EMAIL_FIELD = 'email'
#     # for createsuperuser command will prompt for following
#     # REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'phone_number']
#     REQUIRED_FIELDS = ['phone_number']
#
#     is_active = models.BooleanField(
#         _('is_active'),
#         db_column="Is Active",
#         default=True,
#         help_text=_(
#             "Designates whether this user should be considered active or not."
#         ),
#     )
#
#     # permissions for accessing admin page
#     is_staff = models.BooleanField(
#         _('is_staff'),
#         db_column='Is Staff',
#         default=False,
#         help_text=_(
#             'Designates whether this user is a member of staff to access the admin page or not'
#         )
#     )
#     is_superuser = models.BooleanField(
#         _('is_superuser'),
#         db_column='Is Superuser',
#         default=False,
#         help_text=_(
#             'Designates whether this user has all permissions in the admin page or not'
#         )
#     )
#
#     # custom user model defining username field other than username should define Custom Model Manager
#     objects = UserManager()
#
#     class Meta:
#         db_table = 'auth_user'
#         swappable = 'AUTH_USER_MODEL'
#
#     def __str__(self):
#         "return email_id of user"
#         return self.get_username()
#
#     def get_username(self):
#         "Return the identifying username i.e. phone number for this user"
#         return getattr(self, self.USERNAME_FIELD)
#
#     def get_full_name(self):
#         return self.first_name + ' ' + self.last_name
#
#     # def get_absolute_url(self):
#     #     return reverse('sign-up')
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
