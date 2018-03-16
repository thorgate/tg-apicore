import pytest

from companies.factories import CompanyFactory
from companies.models import User, Employment


@pytest.fixture(scope='function')
def user():
    return User.objects.create_user(
        username='testuser', email='asd@asd.asd', password='test', first_name='Test', last_name='User',
    )


@pytest.fixture(scope='function')
def other_user():
    return User.objects.create_user(
        username='otheruser', email='other@asd.asd', password='test', first_name='Other', last_name='Person',
    )


@pytest.fixture(scope='function')
def company():
    return CompanyFactory.create()


@pytest.fixture(scope='function')
def other_company():
    return CompanyFactory.create()


@pytest.fixture(scope='function')
def employment(user, company):
    return Employment.objects.create(user=user, company=company, role=Employment.ROLE_ADMIN)


@pytest.fixture(scope='function')
def other_employment(other_user, other_company):
    return Employment.objects.create(user=other_user, company=other_company, role=Employment.ROLE_ADMIN)
