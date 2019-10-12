from .models import Film
from django.views import generic


class FilmListView(generic.ListView):
    model = Film


class FilmDetailView(generic.DetailView):
    model = Film

    def get_context_data(self, **kwargs):
        film = Film.objects.get(pk=self.kwargs['pk'])
        poster = film.poster.abs_poster.split('media')[1]
        screens = film.screens.all()
        img = []
        for screen in screens:
            img.append(screen.abs_screen.split('media')[1])
        context = super().get_context_data(**kwargs)
        context['poster'] = poster
        context['screens'] = img
        return context
