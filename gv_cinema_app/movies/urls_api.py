from django.urls import path, re_path

from movies.views import views_api

app_name = 'movies'

urlpatterns = [
    re_path(r'^movies/$', views_api.MoviesAPIIndex.as_view(), name="movies_listing"),
    re_path(r'^movies/(?P<pk>\d+)/$', views_api.MoviesAPIDetail.as_view(), name="movie_detail"),
]
