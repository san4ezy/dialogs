from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mixins import NULLABLE


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

    def create_user(self, phone_number, password=None, username=None):
        if not phone_number:
            raise ValueError("User must have a phone_number")

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    phone_number = models.CharField(_('Phone number'), max_length=16, unique=True, **NULLABLE)
    password = models.CharField(_('Password'), max_length=128)

    first_name = models.CharField(_('First name'), max_length=128, **NULLABLE)
    last_name = models.CharField(_('Last name'), max_length=128, **NULLABLE)
    birthday = models.DateField(_('Birthday'), **NULLABLE)

    is_active = models.BooleanField(_('Active'), default=True)
    is_admin = models.BooleanField(_('Admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"{self.get_full_name() or 'noname'} ({self.phone_number})"

    def get_full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}"

    def get_short_name(self) -> str:
        last_name = self.last_name[0] if self.last_name else ''
        return " ".join([self.first_name or '', last_name])

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    @property
    def is_superuser(self) -> bool:
        return self.is_admin

    @classmethod
    def normalize_username(cls, username) -> str:
        return str(username)

    def extend_token(self, token):
        token['phone_number'] = self.phone_number
        token['first_name'] = self.first_name
        token['last_name'] = self.last_name
        return token

    def make_token(self):
        token = RefreshToken.for_user(self)
        token = self.extend_token(token)
        return token

    def get_tokens(self):
        refresh = self.make_token()
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
