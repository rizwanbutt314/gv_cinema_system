from django.views import generic


class Index(generic.TemplateView):
    template_name = 'movies/index.html'

class Detail(generic.TemplateView):
    template_name = 'movies/detail.html'
