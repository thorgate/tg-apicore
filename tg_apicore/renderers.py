import logging

from rest_framework.renderers import JSONRenderer as DRFJSONRenderer
from rest_framework_json_api.renderers import JSONRenderer as JSONAPIRenderer


logger = logging.getLogger(__name__)


class TransformerAwareJSONRenderer(DRFJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        assert renderer_context
        version_transformers = getattr(renderer_context.get("request"), 'version_transformers', [])
        for transformer in version_transformers:
            data = transformer.output_backwards(data)

        return super().render(data, accepted_media_type, renderer_context)


class JSONRenderer(JSONAPIRenderer, TransformerAwareJSONRenderer):
    """ JSON-API  renderer that uses plain application/json mimetype

    This is intended for easier debugging since browsers don't recognize the custom application/vnd.api+json mimetype.
    """

    media_type = 'application/json'
    format = 'json'


class PureJSONRenderer(DRFJSONRenderer):
    media_type = 'application/json'
    format = 'pure-json'
