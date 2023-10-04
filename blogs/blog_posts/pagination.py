from rest_framework.pagination import PageNumberPagination


class BlogListCreatePagination(PageNumberPagination):
    """
    Apply pagination for the blogs page.
    """
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 50
