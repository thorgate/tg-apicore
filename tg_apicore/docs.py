import json
import logging
from typing import List  # NOQA

from django.utils.safestring import mark_safe

import attr
from rest_framework.utils import encoders


logger = logging.getLogger(__name__)


def jsonize(data):
    return mark_safe(json.dumps(data, cls=encoders.JSONEncoder, indent=2))


@attr.s
class FieldDocs:
    """ Information about a single field of an object (gathered from viewset's serializer) """

    name = attr.ib()
    description = attr.ib()
    is_required = attr.ib()
    is_read_only = attr.ib()
    is_create_only = attr.ib()


@attr.s
class MethodDocs:
    """ Docs for a single API endpoint """

    action = attr.ib()
    request_data = attr.ib(default=None)
    # List of (name, data) tuples
    responses = attr.ib(default=attr.Factory(list))
    docstring = attr.ib(default=None)
    # Relative to API base, filled when generating APIDocs
    path = attr.ib(default=None)
    method = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.docstring = self.docstring or ''

    @property
    def request_data_json(self):
        return jsonize(self.request_data)

    @property
    def responses_items(self):
        # Disable invalid pylint error, this might be fixed in upcoming 1.8.0
        # pylint: disable=not-an-iterable
        return [(name, jsonize(data) if data is not None else None) for name, data in self.responses]


@attr.s
class SectionDocs:
    """ Docs for a section of the API, usually meaning a viewset """

    data = attr.ib(default=None)
    changelog = attr.ib(default=None)
    docstring = attr.ib(default=None)

    name = attr.ib(default=None)  # type: str
    methods = attr.ib(default=attr.Factory(list))  # type: List[MethodDocs]
    hidden_methods = attr.ib(default=attr.Factory(list))  # type: List[str]

    fields = attr.ib(default=attr.Factory(list))  # type: list

    def __attrs_post_init__(self):
        self.docstring = self.docstring or ''

    @property
    def data_json(self):
        return jsonize(self.data)

    @property
    def changelog_items(self):
        return sorted(self.changelog.items(), reverse=True)


@attr.s
class APIDocs:
    """ Docs for the entire API """

    title = attr.ib()  # type: str
    # Longer intro / description text, markdown
    description = attr.ib()  # type: str

    site_url = attr.ib()  # type: str
    base_path = attr.ib()  # type: str

    sections = attr.ib(default=attr.Factory(list))  # type: List[SectionDocs]


def add_api_docs(*docs, hidden_methods=None):
    """ Decorator that adds given list of docs to the class """

    def decorator(cls):
        # Find the section doc and all method docs
        section_doc = None
        method_docs = []
        for doc in docs:
            if isinstance(doc, SectionDocs):
                if section_doc is not None:
                    raise RuntimeError("Only a single SectionDocs instance can be present")
                section_doc = doc
            elif isinstance(doc, MethodDocs):
                method_docs.append(doc)
            else:
                raise RuntimeError("add_api_docs() parameters must be SectionDocs or MethodDocs instances")

        # Create empty section if it wasn't specified
        if section_doc is None:
            section_doc = SectionDocs()

        # Add all found methods to the section and attach the section to the viewset
        section_doc.methods = method_docs

        # Remember hidden methods
        section_doc.hidden_methods = hidden_methods or []

        cls.api_core_docs = section_doc
        return cls

    return decorator


def api_section_docs(*, data=None, changelog=None):
    return SectionDocs(data=data, changelog=changelog)


def api_method_docs(action, *, request_data=None, response_data=None, responses=None, doc=None):
    assert response_data is None or responses is None, "Give either 'response_data' or 'responses', not both"

    responses = responses or []  # type: list
    # Handle convenience inputs. Our canonical format is list of (name, data) tuples, but we also support dicts,
    # as well as just numeric status codes as keys. All of those will be converted into canonical format here.
    if isinstance(responses, dict):
        responses = list(responses.items())
    if response_data is not None:
        responses.append((200, response_data))
    responses = [
        ("Response (status %d)" % response_name if isinstance(response_name, int) else response_name, response_data)
        for response_name, response_data in responses
    ]

    return MethodDocs(action=action, request_data=request_data, responses=responses, docstring=doc)
