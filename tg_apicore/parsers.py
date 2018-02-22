from rest_framework_json_api.parsers import JSONParser as JSONAPIParser

from tg_apicore.renderers import JSONRenderer


class JSONParser(JSONAPIParser):
    media_type = 'application/json'
    renderer_class = JSONRenderer
