from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone_number, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone_number, **extra_fields):
        user = self.create_user(email, password, phone_number, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin,models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    # Add other custom fields as needed

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']  # Add other required fields as needed

    def __str__(self):
        return self.email