import warnings
from urllib.parse import urljoin

from rest_framework.schemas.generators import EndpointEnumerator
from rest_framework.schemas.openapi import SchemaGenerator, AutoSchema


class OptionViewInspector(EndpointEnumerator):
    def get_allowed_methods(self, callback):
        """
        Return a list of the valid HTTP methods for this endpoint.
        """
        if hasattr(callback, 'actions'):
            actions = set(callback.actions)
            http_method_names = set(callback.cls.http_method_names)
            methods = [method.upper() for method in actions & http_method_names]
        else:
            methods = callback.cls().allowed_methods

        return [method for method in methods if method not in ('HEAD',)] + ["OPTIONS"]


class OptionViewSchema(AutoSchema):
    method_mapping = {
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partialUpdate',
        'delete': 'destroy',
        "options": "metadata"
    }

    def get_operation(self, path, method, request=None, view=None):
        operation = super(OptionViewSchema, self).get_operation(path, method)
        if method == "OPTIONS":
            operation['responses'] = self.get_responses(path, method, request=request, view=view)

        return operation

    def get_responses(self, path, method, request=None, view=None):
        if method == "OPTIONS":
            return {
                200: {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string"
                                    },
                                    "renders": {
                                        "type": "array"
                                    },
                                    "schema": {
                                        "type": "object"
                                    },
                                    "ui": {
                                        "type": "object"
                                    },
                                    "fields": {
                                        "type": "array"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        return super(OptionViewSchema, self).get_responses(path, method)


class OptionSchemaGenerator(SchemaGenerator):
    """
    Will generate schema for http OPTION method
    """
    endpoint_inspector_cls = OptionViewInspector

    def get_schema(self, request=None, public=False):
        self._initialise_endpoints()
        components_schemas = {}

        # Iterate endpoints generating per method path operations.
        paths = {}
        _, view_endpoints = self._get_paths_and_endpoints(None if public else request)
        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue

            if method == "OPTIONS" and "{id}" in path:
                continue

            operation = view.schema.get_operation(path, method, request=request, view=view)
            components = view.schema.get_components(path, method)
            for k in components.keys():
                if k not in components_schemas:
                    continue
                if components_schemas[k] == components[k]:
                    continue
                warnings.warn('Schema component "{}" has been overriden with a different value.'.format(k))

            components_schemas.update(components)

            # Normalise path for any provided mount url.
            if path.startswith('/'):
                path = path[1:]
            path = urljoin(self.url or '/', path)

            paths.setdefault(path, {})
            paths[path][method.lower()] = operation

        self.check_duplicate_operation_id(paths)

        # Compile final schema.
        schema = {
            'openapi': '3.0.2',
            'info': self.get_info(),
            'paths': paths,
        }

        if len(components_schemas) > 0:
            schema['components'] = {
                'schemas': components_schemas
            }

        return schema
