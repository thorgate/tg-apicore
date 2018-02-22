import logging
from collections import defaultdict

import attr
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField
from rest_framework.schemas import SchemaGenerator
from rest_framework.utils.formatting import dedent

from tg_apicore.docs import APIDocs, FieldDocs, MethodDocs, SectionDocs


logger = logging.getLogger(__name__)


class ApiDocsGenerator(SchemaGenerator):
    """ Schema generator used for api docs

    Generate APIDocs object, not an ordinary schema. Use `get_docs()` method.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, title, description, patterns, site_url, base_path, urlconf=None):
        super().__init__(title=title, description=description, patterns=patterns, urlconf=urlconf)

        if site_url.endswith('/') and base_path.startswith('/'):
            site_url = site_url[:-1]
        self.site_url = site_url
        self.base_path = base_path

    def get_schema(self, request=None, public=False):
        raise NotImplementedError("Use ApiDocsGenerator.get_docs() instead")

    def get_docs(self):
        if self.endpoints is None:
            inspector = self.endpoint_inspector_cls(self.patterns, self.urlconf)
            self.endpoints = inspector.get_api_endpoints()

        sections = self.get_sections()
        if not sections:
            return None

        return APIDocs(
            title=self.title, description=self.replace_variables(self.description),
            site_url=self.site_url, base_path=self.base_path, sections=sections,
        )

    def get_sections(self, request=None):
        """ Returns list of SectionDocs objects

        Based on SchemaGenerator.get_links()
        """

        # pylint: disable=too-many-locals

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            if getattr(view, 'schema', True) is None:
                continue
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        sections = {}
        section_methods = defaultdict(list)
        for path, method, view in view_endpoints:
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)

            if subpath.startswith('/'):
                subpath = subpath[1:]

            view_cls = view.__class__
            section_name = keys[0]

            # Get or create section doc
            section_doc = sections.get(section_name)
            if section_doc is None:
                section_doc = getattr(view_cls, 'api_core_docs', None)
                if section_doc is None:
                    section_doc = SectionDocs()
                else:
                    # Ensure that we don't change the original
                    section_doc = attr.evolve(section_doc)

                section_doc.fields = self.get_generic_serializer_fields(view)
                if not section_doc.docstring:
                    section_doc.docstring = view_cls.__doc__ or ''
                section_doc.docstring = dedent(section_doc.docstring)
                section_doc.docstring = self.replace_variables(section_doc.docstring)
                section_doc.data = self.replace_variables(section_doc.data)
                if not section_doc.name:
                    section_doc.name = section_name

                sections[section_name] = section_doc

            # Create method doc
            action = keys[1]

            # Skip hidden methods
            if action in section_doc.hidden_methods:
                continue

            method_doc = next((m for m in section_doc.methods if m.action == action), None)
            view_doc = getattr(getattr(view_cls, action, None), '__doc__', '') or ''
            if method_doc is None:
                method_doc = MethodDocs(action=action)

            method_doc = attr.evolve(method_doc, path=subpath, method=method)
            if not method_doc.docstring:
                method_doc.docstring = view_doc
            method_doc.docstring = dedent(method_doc.docstring)
            method_doc.docstring = self.replace_variables(method_doc.docstring)
            method_doc.request_data = self.replace_variables(method_doc.request_data)
            method_doc.responses = self.replace_variables(method_doc.responses)

            section_methods[section_name].append(method_doc)

        # Add all gathered methods to their respective sections
        for section_name in sections:
            sections[section_name].methods = section_methods[section_name]

        return list(sections.values())

    def get_serializer(self, view):
        method = getattr(view, 'get_docs_serializer', None)
        if method is not None:
            return view.get_docs_serializer()

        serializer_class = getattr(view, 'serializer_docs_class', None) or \
            getattr(view, 'serializer_detail_class', None) or getattr(view, 'serializer_class', None)
        if serializer_class is None:
            return None

        return serializer_class(context=view.get_serializer_context())

    def get_generic_serializer_fields(self, view):
        """
        Return a list of `FieldDocs` instances corresponding to any
        request body input, as determined by the serializer class.
        """

        serializer = self.get_serializer(view)
        if serializer is None:
            return None
        if isinstance(serializer, serializers.ListSerializer):
            # TODO?
            return None

        if not isinstance(serializer, serializers.Serializer):
            return []

        create_only_fields = getattr(serializer.Meta, 'create_only_fields', [])
        fields = []
        for field in serializer.fields.values():
            if field.field_name in {'id', 'url'}:
                continue

            # str cast resolves lazy translations
            description = '. '.join([str(x) for x in filter(None, (field.label, field.help_text))])
            is_required = field.required and not isinstance(field, ManyRelatedField)
            is_create_only = field.field_name in create_only_fields
            fields.append(FieldDocs(
                name=field.field_name, description=description,
                is_required=is_required, is_read_only=field.read_only, is_create_only=is_create_only,
            ))

        return fields

    def replace_variables(self, data, **extra_substitutions):
        return replace_variables(data, self.site_url, self.base_path, **extra_substitutions)


def replace_variables(data, site_url, base_path, **extra_substitutions):
    substitutions = {
        'SITE_URL': site_url.rstrip('/'),
        'API_ROOT': (site_url + base_path).rstrip('/'),
    }
    substitutions.update(extra_substitutions)
    return replace_variables_inner(data, substitutions)


def replace_variables_inner(data, substitutions):
    if isinstance(data, str):
        return data % substitutions
    elif isinstance(data, (list, tuple)):
        return [replace_variables_inner(v, substitutions) for v in data]
    elif isinstance(data, dict):
        return {k: replace_variables_inner(v, substitutions) for k, v in data.items()}

    return data


def generate_api_docs(title, description, site_url, base_path, patterns) -> APIDocs:
    generator = ApiDocsGenerator(
        title=title, description=description,
        site_url=site_url, base_path=base_path, patterns=patterns,
    )
    return generator.get_docs()
