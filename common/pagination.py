from rest_framework import pagination
from rest_framework.response import Response


class TotalPageCountPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response_schema(self, schema):
        prev_schema = super().get_paginated_response_schema(schema)
        prev_schema["properties"]["currentPage"] = {
            'type': 'integer',
            "description": "Current page number",
            'example': 123,
        }
        prev_schema["properties"]["totalPages"] = {
            'type': 'integer',
            "description": "Total number of pages",
            'example': 123,
        }

        return prev_schema

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            "currentPage": self.page.number,
            "totalPages": self.page.paginator.num_pages,
            'results': data
        })
