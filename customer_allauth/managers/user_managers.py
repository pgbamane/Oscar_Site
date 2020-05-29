# from django.contrib.auth.models import BaseUserManager
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, phone_number, email, password=None, **extra_fields):
#         email = self.normalize_email(email)
#         customer_final = self.model(phone_number=phone_number, email=email, **extra_fields)
#         customer_final.is_active = True
#         customer_final.set_password(raw_password=password)
#         customer_final.save()
#         return customer_final
#
#     def create_superuser(self, phone_number, email, password=None, **extra_fields):
#         customer_final = self.create_user(phone_number, email, password, **extra_fields)
#         customer_final.is_active = True
#         customer_final.is_superuser = True
#         customer_final.is_staff = True
#         customer_final.save()
#         return customer_final
#
#     def create_staffuser(self, phone_number, email, password=None, **extra_fields):
#         customer_final = self.create_user(phone_number, email, password, **extra_fields)
#         customer_final.is_active = True
#         customer_final.is_staff = True
#         customer_final.save()
#         return customer_final
