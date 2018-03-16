import random

import factory
from factory.django import DjangoModelFactory

from companies.models import User, Company, Employment


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
    reg_code = factory.Faker('numerify', text='%##-####')


def create_full_example_data():
    UserFactory.create_batch(100)
    CompanyFactory.create_batch(70)

    users = list(User.objects.all())
    companies = list(Company.objects.all())

    # Generate 300 unique user-company pairs
    user_company_pairs = set()
    while len(user_company_pairs):
        user_company_pairs.add((random.choice(users), random.choice(companies)))

    Employment.objects.bulk_create([
        Employment(user=user, company=company,
                   role=Employment.ROLE_ADMIN if random.random() < 0.25 else Employment.ROLE_NORMAL)
        for user, company in user_company_pairs
    ])
