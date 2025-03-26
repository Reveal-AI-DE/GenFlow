# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import sys
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    '''
    Custom pagination class that extends PageNumberPagination to allow dynamic page size.

    Methods:
        get_page_size(request):
            Retrieves the page size from the request query parameters.
            If the query parameter value is 'all', it sets the page size to the maximum integer value.
            If the query parameter value is not a valid integer or is missing, it falls back to the default page size.
            Returns the page size as an integer.
    '''

    page_size_query_param = "page_size"

    def get_page_size(self, request):
        page_size = 0
        try:
            value = request.query_params[self.page_size_query_param]
            if value == 'all':
                page_size = sys.maxsize
            else:
                page_size = int(value)
        except (KeyError, ValueError):
            pass

        return page_size if page_size > 0 else self.page_size
