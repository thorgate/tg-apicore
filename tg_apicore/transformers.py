import logging


logger = logging.getLogger(__name__)


class VersionTransformer:
    """ Base class for transforming API requests/responses between versions

    Each transformer is responsible for converting input (request data) from one version to the next one,
    and for converting output (response data) from the next version to this one.

    This way API views/serializers/etc can be written to always target only the latest version, and each earlier version
    has one or more transformers that convert data between the two versions.
    When the version history gets longer, requests and responses can be transformed by multiple transformers in
    sequence.

    Inspired by https://github.com/mrhwick/django-rest-framework-version-transforms and
    https://stripe.com/blog/api-versioning
    """

    @classmethod
    def is_applicable(cls, model, action) -> bool:
        return True

    def __init__(self, model, action) -> None:
        super().__init__()
        self.model = model
        self.action = action

    def input_forwards(self, data):
        return data

    def output_backwards(self, data):
        return data

    def convert_output_object(self, obj_type, obj_id, fields):
        raise NotImplementedError()

    def convert_output_object_container(self, data):
        if 'type' not in data or 'id' not in data or 'attributes' not in data:
            return data
        res = self.convert_output_object(data['type'], data['id'], data['attributes'])

        if res is None:
            return data

        data['attributes'] = res
        return data

    def convert_all_output_objects(self, response):
        data = response.get('data')

        if isinstance(data, dict):
            response['data'] = self.convert_output_object_container(data)
        elif isinstance(data, (list, tuple)):
            response['data'] = [self.convert_output_object_container(obj) for obj in data]
        else:
            return response

        if 'included' in response:
            response['included'] = [self.convert_output_object_container(obj) for obj in response['included']]

        return response


# TODO: move out of here
TRANSFORMS = [
]


def get_transformers(request_version, model, action):
    transformers = []
    for version, version_transformers in TRANSFORMS:
        if version <= request_version:
            break
        for t in version_transformers:
            if t.is_applicable(model, action):
                transformers.append(t)

    return [t(model, action) for t in transformers]
