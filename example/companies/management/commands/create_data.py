import random

from django.core.management.base import BaseCommand

import factory
from factory.django import DjangoModelFactory

from companies.models import User, Company, Employment


def faker_with_max_length(provider: str, max_length: int):
    return factory.LazyFunction(lambda: factory.Faker(provider).generate({})[:max_length])


def faker_estonian_phone_number():
    """ Creates valid Estonian phone numbers.
    Numbers beginning with '+37250', followed by 5 or 6 digits are always valid.
    """
    return factory.LazyFunction(lambda: ('+37250%06d' % random.randint(0, 999999)))


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = factory.PostGenerationMethodCall('set_password', 'test')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('company')
    email = factory.Faker('email')


class Command(BaseCommand):
    help = "Create test data"

    def handle(self, *args, **options):
        UserFactory.create_batch(100)
        CompanyFactory.create_batch(70)

        users = list(User.objects.all())
        companies = list(Company.objects.all())

        Employment.objects.bulk_create([
            Employment(user=random.choice(users), company=random.choice(companies),
                       role=Employment.ROLE_MANAGER if random.random() < 0.25 else Employment.ROLE_NORMAL)
            for _ in range(300)
        ])
