from django.db.models import Model

from rest_framework.utils import model_meta
from rest_framework_json_api import serializers


class CreateOnlyFieldsSerializerMixin:
    """ Adds support for fields that can only be specified at object creation time.

    Serializer fields can be marked as create-only by listing them in Meta.create_only_fields - these are
    read-only for existing instances but can be specified at object creation time.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If we have an existing instance, mark the create-only fields as read-only.
        if not getattr(self, 'many', False) and isinstance(self.instance, Model) and self.instance.pk is not None:
            create_only_fields = getattr(self.Meta, 'create_only_fields', [])
            for field_name in create_only_fields:
                self.fields[field_name].read_only = True


class ModelValidationSerializerMixin:
    """ Uses validation logic defined in the model class

    By default, DRF has it's own validation logic, separate from the one defined in the model.
    This tries to bridge the two, ensuring that's model's full_clean() also gets called.

    It's quite hacky as there doesn't seem to be a very straightforward way of accomplishing this.

    Also note that it makes an extra database query when validate() is called for an existing instance.
    """

    def validate(self, attrs):
        attrs = super().validate(attrs)

        self.run_model_validation(attrs)

        return attrs

    def run_model_validation(self, attrs: dict):
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the model's `.__init__()` method,
        # as they require that the instance has already been saved.
        attrs = attrs.copy()
        info = model_meta.get_field_info(ModelClass)
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in attrs):
                attrs.pop(field_name)

        # We don't want to modify self.instance, so either create new instance or fetch the existing one from DB
        if self.instance is None:
            obj = ModelClass(**attrs)
        else:
            try:
                obj = ModelClass.objects.get(pk=self.instance.pk)
            except ModelClass.DoesNotExist:
                # If the model cannot be retrieved, just skip the extra validation step
                return

            # Update the fetched object with values from attrs
            for k, v in attrs.items():
                setattr(obj, k, v)

        # Run model validation logic
        obj.full_clean()


class BaseModelSerializer(CreateOnlyFieldsSerializerMixin, ModelValidationSerializerMixin, serializers.ModelSerializer):
    """ Combines JSON-API model serializer with create-only fields and model validation.
    """
