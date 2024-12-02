from rest_framework.pagination import PageNumberPagination

class PeraturanVersionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        size = request.query_params.get(self.page_size_query_param)
        if size and size.isdigit():
            size = int(size)
            return min(size, self.max_page_size)
        return super().get_page_size(request)