from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/?', include('movies.urls_api', namespace='movies_api')),
    url(r'^', include('movies.urls_ui', namespace='movies_ui')),
]
