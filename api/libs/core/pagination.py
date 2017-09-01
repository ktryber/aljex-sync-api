from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasicPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        next_page = None
        previous_page = None

        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('current', self.page.number),
            ('next', next_page),
            ('previous', previous_page),
            ('results', data),
        ]))
