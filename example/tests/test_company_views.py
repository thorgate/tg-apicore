from copy import deepcopy

import pytest

from tg_apicore.test import APIClient, validate_jsonapi_detail_response, validate_jsonapi_list_response, \
    validate_jsonapi_error_response, validate_response_status_code

from companies.api_docs import COMPANIES_CREATE_REQUEST
from companies.factories import CompanyFactory
from companies.models import Company, Employment, User


ATTRIBUTES_LIST = {'created', 'updated', 'reg_code', 'name', 'email'}
RELATIONSHIPS_LIST = set()
ATTRIBUTES_PUBLIC = ATTRIBUTES_LIST
RELATIONSHIPS_PUBLIC = RELATIONSHIPS_LIST
ATTRIBUTES_FULL = ATTRIBUTES_LIST
RELATIONSHIPS_FULL = {'employees'}


def do_test_company_listing(client: APIClient, batch_size=5):
    CompanyFactory.create_batch(batch_size)

    resp = client.get(client.reverse('company-list'))
    validate_jsonapi_list_response(
        resp, expected_count=batch_size, expected_attributes=ATTRIBUTES_LIST,
        expected_relationships=RELATIONSHIPS_LIST,
    )


@pytest.mark.django_db
def test_create_company(user: User):
    """ Users should be able to create companies. They should become admin of the created company.
    """

    client = APIClient()
    client.force_authenticate(user)

    resp = client.post(client.reverse('company-list'), data=COMPANIES_CREATE_REQUEST)
    data = validate_jsonapi_detail_response(resp, expected_status_code=201)

    assert Employment.objects.filter(user=user,  company_id=data['data']['id'], role=Employment.ROLE_ADMIN).exists()


@pytest.mark.django_db
def test_create_company_public():
    """ Companies cannot be created by anonymous users.
    """

    client = APIClient()

    resp = client.post(client.reverse('company-list'), data=COMPANIES_CREATE_REQUEST)
    validate_jsonapi_error_response(resp, expected_status_code=403)


@pytest.mark.django_db
def test_companies_list(user: User):
    """ Companies can be listed by a user.
    """

    client = APIClient()
    client.force_authenticate(user)

    do_test_company_listing(client)


@pytest.mark.django_db
def test_companies_list_public():
    """ Companies can also be listed anonymously.
    """

    client = APIClient()
    do_test_company_listing(client)


@pytest.mark.django_db
def test_companies_details_employee(employment: Employment):
    """ Company details can be viewed by an employee, and full information is returned.
    """

    client = APIClient()
    client.force_authenticate(employment.user)

    resp = client.get(client.reverse('company-detail', pk=employment.company.pk))
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_FULL, expected_relationships=RELATIONSHIPS_FULL,
    )


@pytest.mark.django_db
def test_companies_details_unrelated(user: User, other_company: Company):
    """ Company details can be viewed by an unrelated user (non-employee), but only basic information is returned.
    """

    client = APIClient()
    client.force_authenticate(user)

    resp = client.get(client.reverse('company-detail', pk=other_company.pk))
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_PUBLIC, expected_relationships=RELATIONSHIPS_PUBLIC,
    )


@pytest.mark.django_db
def test_companies_details_public(company: Company):
    """ Company details can also be viewed anonymously, only basic information is returned.
    """

    client = APIClient()

    resp = client.get(client.reverse('company-detail', pk=company.pk))
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_PUBLIC, expected_relationships=RELATIONSHIPS_PUBLIC,
    )


@pytest.mark.django_db
def test_companies_update(employment: Employment):
    assert employment.role == Employment.ROLE_ADMIN
    user = employment.user
    company = employment.company

    client = APIClient()
    client.force_authenticate(user)

    other_company = CompanyFactory.create()

    patch_data = {
        "data": {
            "type": "company",
            "id": str(company.id),
            "attributes": {},
        },
    }

    # Part one - update the company where the user is admin
    new_name = 'new name'
    updated = company.updated
    assert company.name != new_name
    patch_data['data']['attributes'] = {'name': new_name}
    resp = client.patch(client.reverse('company-detail', pk=company.pk), patch_data)
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_FULL, expected_relationships=RELATIONSHIPS_FULL,
    )
    refreshed_company = Company.objects.get(id=company.id)
    assert refreshed_company.name == new_name
    assert refreshed_company.updated > updated

    # Part two - PUT should not be allowed
    resp = client.put(client.reverse('company-detail', pk=company.pk), patch_data)
    validate_jsonapi_error_response(resp, expected_status_code=405)

    # Part three - updating is only allowed for admins, so it should fail after user is demoted to non-admin
    employment.role = Employment.ROLE_NORMAL
    employment.save()
    resp = client.patch(client.reverse('company-detail', pk=company.pk), patch_data)
    validate_jsonapi_error_response(resp, expected_status_code=403)

    # Part four - try to patch company where we don't have permissions
    patch_data['data']['id'] = str(other_company.id)
    resp = client.patch(client.reverse('company-detail', pk=other_company.pk))
    validate_jsonapi_error_response(resp, expected_status_code=403)


@pytest.mark.django_db
def test_companies_create_only_fields(user: User):
    """ Ensures that create-only fields cannot be updated for existing instances.

    It also acts as general test for the create-only fields functionality.
    """

    client = APIClient()
    client.force_authenticate(user)

    # Part one - try creating a company without reg_code (required and create-only field) - this should fail
    req_data = deepcopy(COMPANIES_CREATE_REQUEST)
    del req_data['data']['attributes']['reg_code']
    resp = client.post(client.reverse('company-list'), data=req_data)
    validate_jsonapi_error_response(resp, expected_status_code=400)

    # Part two - create a company with all the necessary fields
    req_data = deepcopy(COMPANIES_CREATE_REQUEST)
    resp = client.post(client.reverse('company-list'), data=req_data)
    resp_data = validate_jsonapi_detail_response(resp, expected_status_code=201)

    # Ensure everything is as intended
    req_data_attributes = req_data['data']['attributes']
    company = Company.objects.get(id=resp_data['data']['id'])
    for attr_name in req_data_attributes:
        assert getattr(company, attr_name) == req_data_attributes[attr_name]

    # Next, try updating the reg_code, which should be read-only
    new_reg_code = 123456
    assert company.reg_code != new_reg_code
    patch_data = {
        "data": {
            "type": "company",
            "id": str(company.id),
            "attributes": {
                'reg_code': new_reg_code,
            },
        },
    }

    # Try to update the value - it should be no-op
    resp = client.patch(client.reverse('company-detail', pk=company.pk), patch_data)
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_FULL, expected_relationships=RELATIONSHIPS_FULL,
    )
    # Ensure the value in database hasn't been changed
    refreshed_company = Company.objects.get(id=company.id)
    assert refreshed_company.reg_code == company.reg_code


@pytest.mark.django_db
def test_companies_delete(employment: Employment, other_company: Company):
    """ Ensures admins can delete companies but non-admin employees cannot.
    """

    assert employment.role == Employment.ROLE_ADMIN
    user = employment.user
    company = employment.company

    client = APIClient()
    client.force_authenticate(user)

    # Part one - delete the company where the user is admin
    resp = client.delete(client.reverse('company-detail', pk=company.id))
    validate_response_status_code(resp, 204)
    assert not Company.objects.filter(id=company.id).exists()

    # Part two - try to delete an unrelated company - this should not be allowed
    resp = client.delete(client.reverse('company-detail', pk=other_company.id))
    validate_jsonapi_error_response(resp, expected_status_code=403)
    assert Company.objects.filter(id=other_company.id).exists()
