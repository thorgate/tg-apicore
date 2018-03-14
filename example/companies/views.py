from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet

from companies import api_docs
from companies.models import Company, Employment
from companies.serializers import CompanySerializer, EmploymentSerializer, CompanySummarySerializer, \
    EmploymentSummarySerializer
from tg_apicore.docs import add_api_docs, api_section_docs, api_method_docs
from tg_apicore.viewsets import DetailSerializerViewSet


@add_api_docs(
    api_section_docs(
        data=api_docs.COMPANIES_DATA,
    ),
    api_method_docs(
        'list',
        response_data=api_docs.COMPANIES_LIST_RESPONSE,
    ),
    api_method_docs(
        'create',
        request_data=api_docs.COMPANIES_CREATE_REQUEST,
        responses=api_docs.COMPANIES_CREATE_RESPONSES,
    ),
    api_method_docs(
        'retrieve',
        response_data=api_docs.COMPANIES_READ_RESPONSE,
    ),
    api_method_docs(
        'destroy',
        responses=api_docs.COMPANIES_DELETE_RESPONSES,
    ),
)
class CompanyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, ReadOnlyModelViewSet, DetailSerializerViewSet):
    """ Companies API - provides CRUD functionality for companies.

    Employees information is included in responses.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySummarySerializer
    serializer_detail_class = CompanySerializer

    # pylint: disable=useless-super-delegation
    def list(self, request, *args, **kwargs):
        """ List all companies.
        """

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Creates a new company.
        """

        return super().create(request, *args, **kwargs)

    # pylint: disable=useless-super-delegation
    def destroy(self, request, *args, **kwargs):
        """ Deletes the given company.
        """
        return super().destroy(request, *args, **kwargs)


@add_api_docs(
)
class EmploymentViewSet(ReadOnlyModelViewSet, DetailSerializerViewSet):
    """ Employments API
    """

    queryset = Employment.objects.all()
    serializer_class = EmploymentSummarySerializer
    serializer_detail_class = EmploymentSerializer

    # pylint: disable=useless-super-delegation
    def list(self, request, *args, **kwargs):
        """ List all employments.
        """

        return super().list(request, *args, **kwargs)
