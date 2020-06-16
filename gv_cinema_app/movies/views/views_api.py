from django.db.models import Prefetch
from rest_framework import mixins, generics, filters, status

from movies.models import Movies
from movies.serializers import MoviesSerializer
from gv_cinema_app.common.pagination import ApiResultsSetPagination


class MoviesAPIIndex(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = MoviesSerializer
    pagination_class = ApiResultsSetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return Movies.objects.all().select_related('language'). \
            prefetch_related(Prefetch('genre', to_attr='genre_list'))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MoviesAPIDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    serializer_class = MoviesSerializer
    queryset = Movies.objects.all().select_related('language'). \
        prefetch_related(Prefetch('genre', to_attr='genre_list'))

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
