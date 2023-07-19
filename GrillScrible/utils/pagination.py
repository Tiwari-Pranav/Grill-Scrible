from rest_framework.pagination import PageNumberPagination

class ListPageNumberPagination(PageNumberPagination):
    page_size=9
    
    def __init__(self, page_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if page_size is not None:
            self.page_size = page_size