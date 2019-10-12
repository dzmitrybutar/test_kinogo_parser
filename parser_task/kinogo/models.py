from django.db import models
from django.urls import reverse


class Film(models.Model):
    title = models.CharField(blank=False, max_length=128)
    url = models.URLField(blank=True, max_length=128)
    year = models.CharField(blank=True, max_length=4)
    desc = models.TextField(blank=True, max_length=2048)
    duration = models.CharField(blank=True, max_length=8)
    genres = models.CharField(blank=True, max_length=128)

    def get_absolute_url(self):
        return reverse('film_details', args=[str(self.id)])

    class Meta:
        ordering = ['title']


class Poster(models.Model):
    abs_poster = models.CharField(blank=True, max_length=128)
    films = models.OneToOneField(Film, on_delete=models.CASCADE, related_name='poster')


class Screen(models.Model):
    abs_screen = models.TextField(blank=True, max_length=1024)
    films = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screens')
