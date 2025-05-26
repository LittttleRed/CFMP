from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """默认每页20个，最多100个"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100