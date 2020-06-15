from django.urls import path, re_path

from movies.views import views_ui

app_name='movies'

urlpatterns = [
    re_path(r'^$', views_ui.Index.as_view(), name="movies_listing_ui"),
    re_path(r'^detail/(?P<pk>\d+)/$', views_ui.Detail.as_view(), name="movie_detail_ui"),
]