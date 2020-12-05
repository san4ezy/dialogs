import random
import factory
import factory.fuzzy
from django.contrib.auth.models import Group
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile

from faker import Faker
from factory.django import DjangoModelFactory

from apps.utils import get_lorem_ipsum

DEFAULT_PASSWORD = "password"
WRONG_PASSWORD = "wrong-password"

fake = Faker()


def make_name(*args, **kwargs):
    return f"{fake.first_name()} {fake.last_name()}"


def make_first_name(*args, **kwargs):
    return fake.first_name()


def make_last_name(*args, **kwargs):
    return fake.last_name()


def make_email(*args, **kwargs):
    email = f"{fake.first_name()}.{fake.last_name()}@example.com".lower()
    if len(email) > 64:
        email = email[len(email)-32:]
    return email


def make_phone_number(*args, **kwargs):
    codes = (50, 95, 99, 66, 67, 97, 96, 98, 68, 63, 93, 73, )
    return f"+380{random.choice(codes)}{random.randint(1000000, 9999999)}"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ('phone_number',)

    phone_number = factory.LazyAttribute(make_phone_number)
    first_name = factory.LazyAttribute(make_first_name)
    last_name = factory.LazyAttribute(make_last_name)
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
    is_active = True
    is_admin = False
