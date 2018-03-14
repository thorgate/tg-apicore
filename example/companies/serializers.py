from rest_framework_json_api import serializers

from tg_apicore.serializers import BaseModelSerializer

from companies.models import Company, Employment


class EmploymentSummarySerializer(BaseModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', 'url', 'created', 'name', 'email', 'role']

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email


class CompanySummarySerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'url', 'created', 'name', 'email']


class EmploymentSerializer(EmploymentSummarySerializer):
    class Meta(EmploymentSummarySerializer.Meta):
        fields = EmploymentSummarySerializer.Meta.fields + ['company']

    class JSONAPIMeta:
        included_resources = ['company']

    included_serializers = {
        'company': CompanySummarySerializer,
    }


class CompanySerializer(CompanySummarySerializer):
    class Meta(CompanySummarySerializer.Meta):
        fields = CompanySummarySerializer.Meta.fields + ['employees']

    class JSONAPIMeta:
        included_resources = ['employees']

    included_serializers = {
        'employees': EmploymentSummarySerializer,
    }
