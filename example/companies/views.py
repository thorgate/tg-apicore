from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tg_apicore.docs import add_api_docs, api_section_docs, api_method_docs
from tg_apicore.viewsets import DetailSerializerViewSet

from companies import api_docs
from companies.models import Company, Employment
from companies.serializers import CompanySerializer, EmploymentSerializer, CompanySummarySerializer, \
    EmploymentSummarySerializer


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
        doc="Retrieve details of a specific company. If you're an employee of that company, it will also include "
            "employees info.",
        response_data=api_docs.COMPANIES_READ_RESPONSE,
    ),
    api_method_docs(
        'partial_update',
        doc="Updates company data. You need to be admin employee to do that.",
        request_data=api_docs.COMPANIES_UPDATE_REQUEST,
        responses=api_docs.COMPANIES_READ_RESPONSE,
    ),
    api_method_docs(
        'destroy',
        responses=api_docs.COMPANIES_DELETE_RESPONSES,
    ),
)
class CompanyViewSet(ModelViewSet, DetailSerializerViewSet):
    """ Companies API - provides CRUD functionality for companies.

    If a user creates a company, they'll automatically become employee of that company, in admin role.

    Basic information about companies can be viewed by everyone.
    Employee info can be seen only by employees, in detail responses.
    Changes can be made only by admins.
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Company.objects.all()
    serializer_class = CompanySummarySerializer
    serializer_detail_class = CompanySerializer  # only for employees, see get_detail_serializer_class()
    serializer_modify_class = CompanySerializer

    def get_detail_serializer_class(self):
        # Detail serializer is only for employees
        company = self.get_object()
        user = self.request.user
        if company is not None and user.is_authenticated and \
                Employment.objects.filter(company=company, user=user).exists():
            return self.serializer_detail_class

        return self.get_list_serializer_class()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        # Unsafe methods (= editing) can be used only by managers
        if request.method not in SAFE_METHODS:
            if not Employment.objects.filter(company=obj, user=request.user, role=Employment.ROLE_ADMIN).exists():
                self.permission_denied(request)

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

    def perform_create(self, serializer):
        """ Adds current user as admin of the created company.
        """

        super().perform_create(serializer)

        company = serializer.instance
        Employment.objects.create(company=company, user=self.request.user, role=Employment.ROLE_ADMIN)


@add_api_docs(
    api_section_docs(
        data=api_docs.EMPLOYMENTS_DATA,
    ),
    api_method_docs(
        'list',
    ),
    api_method_docs(
        'create',
        request_data=api_docs.EMPLOYMENTS_CREATE_REQUEST,
        responses=api_docs.EMPLOYMENTS_CREATE_RESPONSES,
    ),
)
class EmploymentViewSet(ModelViewSet, DetailSerializerViewSet):
    """ Employee management API.

    Employees can only be changed by admins of a company, and can be viewed by all employees of a company.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Employment.objects.all()
    serializer_class = EmploymentSummarySerializer
    serializer_detail_class = EmploymentSerializer

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        # Unsafe methods (= editing) can be used only by managers
        if request.method not in SAFE_METHODS:
            if not Employment.objects.filter(company_id=obj.company_id, user=request.user, role=Employment.ROLE_ADMIN) \
                    .exists():
                self.permission_denied(request)

    def get_list_queryset(self):
        user_companies = Employment.objects.filter(user=self.request.user).values_list('company_id', flat=True)
        return super().get_list_queryset().filter(company__in=user_companies)
