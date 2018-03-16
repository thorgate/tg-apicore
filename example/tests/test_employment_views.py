from copy import deepcopy

import pytest

from tg_apicore.test import APIClient, validate_jsonapi_detail_response, validate_jsonapi_list_response, \
    validate_jsonapi_error_response, validate_response_status_code

from companies.api_docs import EMPLOYMENTS_CREATE_REQUEST
from companies.models import Company, Employment, User


ATTRIBUTES_LIST = {'created', 'updated', 'name', 'email', 'role'}
RELATIONSHIPS_LIST = set()
ATTRIBUTES_FULL = ATTRIBUTES_LIST
RELATIONSHIPS_FULL = {'company'}


def get_employment_create_data_for(company: Company, email: str):
    req_data = deepcopy(EMPLOYMENTS_CREATE_REQUEST)
    req_data['data']['relationships']['company']['data']['id'] = str(company.id)
    req_data['data']['attributes']['email'] = email

    return req_data


@pytest.mark.django_db
def test_create_employment(employment: Employment):
    """ Admin users should be able to create employments in the same company.
    """

    company = employment.company
    user = employment.user
    assert employment.role == Employment.ROLE_ADMIN

    email = 'anotheruser@foo.bar'
    assert not User.objects.filter(email=email).exists()

    client = APIClient()
    client.force_authenticate(user)

    req_data = get_employment_create_data_for(company, email)
    resp = client.post(client.reverse('employment-list'), data=req_data)
    validate_jsonapi_detail_response(resp, expected_status_code=201)

    assert User.objects.filter(email=email).exists()
    assert Employment.objects.filter(user=user,  company=company, role=Employment.ROLE_ADMIN).exists()


@pytest.mark.django_db
def test_create_employment_nonadmin(employment: Employment):
    """ Users who are not admin in a company cannot create employments for that company.
    """

    company = employment.company
    user = employment.user
    employment.role = Employment.ROLE_NORMAL
    employment.save()

    client = APIClient()
    client.force_authenticate(user)

    req_data = get_employment_create_data_for(company, 'anotheruser@foo.bar')

    resp = client.post(client.reverse('employment-list'), data=req_data)
    validate_jsonapi_error_response(resp, expected_status_code=400)


@pytest.mark.django_db
def test_create_employment_unrelated(user: User, other_company: Company):
    """ Users who are not employees of a company cannot create employments for that company.
    """

    client = APIClient()
    client.force_authenticate(user)

    req_data = get_employment_create_data_for(other_company, 'anotheruser@foo.bar')

    resp = client.post(client.reverse('employment-list'), data=req_data)
    validate_jsonapi_error_response(resp, expected_status_code=400)


@pytest.mark.django_db
def test_create_employment_public(company: Company):
    """ Employments cannot be created by anonymous users.
    """

    client = APIClient()

    req_data = get_employment_create_data_for(company, 'anotheruser@foo.bar')

    resp = client.post(client.reverse('employment-list'), data=req_data)
    validate_jsonapi_error_response(resp, expected_status_code=403)


@pytest.mark.django_db
def test_employments_list(employment: Employment, other_user: User, other_company: Company):
    """ Employments can be listed by existing employees of a company.
    Users should see only employees of companies they themselves belong to.
    """

    user = employment.user

    client = APIClient()
    client.force_authenticate(user)

    Employment.objects.create(company=other_company, user=other_user, role=Employment.ROLE_ADMIN)
    assert Employment.objects.count() == 2

    # Ensure we only get a single employment back - the one belonging to the company we're in.
    resp = client.get(client.reverse('employment-list'))
    resp_data = validate_jsonapi_list_response(
        resp, expected_count=1,
        expected_attributes=ATTRIBUTES_LIST, expected_relationships=RELATIONSHIPS_LIST,
    )
    assert set(item['id'] for item in resp_data['data']) == {str(employment.company_id)}


@pytest.mark.django_db
def test_employments_list_public():
    """ Employees cannot be listed anonymously.
    """

    client = APIClient()

    resp = client.get(client.reverse('employment-list'))
    validate_jsonapi_error_response(resp, 403)


@pytest.mark.django_db
def test_employments_details_employee(employment: Employment, other_user: User):
    """ Employment details can be viewed by an employee, and full information is returned.
    """

    company = employment.company
    other_employment = Employment.objects.create(company=company, user=other_user, role=Employment.ROLE_NORMAL)

    client = APIClient()
    client.force_authenticate(employment.user)

    resp = client.get(client.reverse('employment-detail', pk=other_employment.pk))
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_FULL, expected_relationships=RELATIONSHIPS_FULL,
    )


@pytest.mark.django_db
def test_employments_details_unrelated(user: User, other_employment: Employment):
    """ Employment details cannot be viewed by an unrelated user (non-employee).
    """

    client = APIClient()
    client.force_authenticate(user)

    resp = client.get(client.reverse('employment-detail', pk=other_employment.pk))
    validate_jsonapi_error_response(resp, 404)


@pytest.mark.django_db
def test_employments_details_public(other_employment: Employment):
    """ Employment details cannot be viewed anonymously.
    """

    client = APIClient()

    resp = client.get(client.reverse('employment-detail', pk=other_employment.pk))
    validate_jsonapi_error_response(resp, 403)


@pytest.mark.django_db
def test_employments_update(employment: Employment, other_user: User):
    """ Admins should be able to update employment info (= role) of companies where they are admins.
    """

    assert employment.role == Employment.ROLE_ADMIN
    user = employment.user
    company = employment.company
    other_employment = Employment.objects.create(company=company, user=other_user, role=Employment.ROLE_NORMAL)

    client = APIClient()
    client.force_authenticate(user)

    patch_data = {
        "data": {
            "type": "employment",
            "id": str(other_employment.id),
            "attributes": {},
        },
    }

    # Part one - update the employment, changing role to admin
    updated = other_employment.updated
    patch_data['data']['attributes'] = {'role': Employment.ROLE_ADMIN}
    resp = client.patch(client.reverse('employment-detail', pk=other_employment.pk), patch_data)
    validate_jsonapi_detail_response(
        resp,
        expected_attributes=ATTRIBUTES_FULL, expected_relationships=RELATIONSHIPS_FULL,
    )
    refreshed_employment = Employment.objects.get(id=other_employment.id)
    assert refreshed_employment.role == Employment.ROLE_ADMIN
    assert refreshed_employment.updated > updated

    # Part two - PUT should not be allowed
    resp = client.put(client.reverse('employment-detail', pk=other_employment.pk), patch_data)
    validate_jsonapi_error_response(resp, expected_status_code=405)

    # Part three - updating is only allowed for admins, so it should fail after user is demoted to non-admin
    employment.role = Employment.ROLE_NORMAL
    employment.save()
    resp = client.patch(client.reverse('employment-detail', pk=other_employment.pk), patch_data)
    validate_jsonapi_error_response(resp, expected_status_code=403)


@pytest.mark.django_db
def test_employments_delete(employment: Employment, other_user: User, other_employment: Employment):
    """ Ensures admins can delete employments but non-admin employees cannot.
    """

    assert employment.role == Employment.ROLE_ADMIN
    user = employment.user
    company = employment.company
    target_employment = Employment.objects.create(company=company, user=other_user, role=Employment.ROLE_NORMAL)

    client = APIClient()
    client.force_authenticate(user)

    # Part one - delete the company where the user is admin
    resp = client.delete(client.reverse('employment-detail', pk=target_employment.id))
    validate_response_status_code(resp, 204)
    assert not Employment.objects.filter(id=target_employment.id).exists()

    # Part two - try to delete an unrelated company - this should not be allowed
    resp = client.delete(client.reverse('employment-detail', pk=other_employment.id))
    validate_jsonapi_error_response(resp, expected_status_code=404)
    assert Employment.objects.filter(id=other_employment.id).exists()
