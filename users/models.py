from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def create_user(self, phone_number, first_name="", last_name="", password=None):
        if not password:
            raise ValueError('password is required')
        if not phone_number:
            raise ValueError('phone number is required')
        user = self.model(phone_number=phone_number)
        user.username = phone_number
        user.password = make_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number=phone_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

# Create your models here.
