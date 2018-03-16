from rest_framework_json_api import serializers

from tg_apicore.serializers import BaseModelSerializer

from companies.models import Company, Employment, User


class EmploymentSummarySerializer(BaseModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', 'url', 'created', 'updated', 'name', 'email', 'role']
        create_only_fields = ['email']

    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email')


class CompanySummarySerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'url', 'created', 'updated', 'reg_code', 'name', 'email']
        create_only_fields = ['reg_code']


class EmploymentSerializer(EmploymentSummarySerializer):
    class Meta(EmploymentSummarySerializer.Meta):
        fields = EmploymentSummarySerializer.Meta.fields + ['company']

    class JSONAPIMeta:
        included_resources = ['company']

    included_serializers = {
        'company': CompanySummarySerializer,
    }

    def validate_company(self, value):
        user = self.context['request'].user
        if not Employment.objects.filter(company=value, user=user, role=Employment.ROLE_ADMIN).exists():
            raise serializers.ValidationError("You are not admin in the specified company", code='user_not_admin')

        return value

    def validate(self, attrs):
        # If user's email was given, use it to look up the actual object (creating it if necessary)
        if attrs.get('user', {}).get('email'):
            attrs['user'], _ = User.objects.get_or_create(email=attrs.pop('user')['email'])

        return super().validate(attrs)


class CompanySerializer(CompanySummarySerializer):
    class Meta(CompanySummarySerializer.Meta):
        fields = CompanySummarySerializer.Meta.fields + ['employees']
        read_only_fields = ['employees']

    class JSONAPIMeta:
        included_resources = ['employees']

    included_serializers = {
        'employees': EmploymentSummarySerializer,
    }
