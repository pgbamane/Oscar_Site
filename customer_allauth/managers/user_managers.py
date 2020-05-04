from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.is_active = True
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        user = self.create_user(phone_number, email, password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_staffuser(self, phone_number, email, password=None, **extra_fields):
        user = self.create_user(phone_number, email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.save()
        return user
