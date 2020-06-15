from django.db import models
from django.contrib.postgres.fields import JSONField


class Genre(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Name of Genre")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Name of Language")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Movies(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Name of Movie")
    description = models.TextField(
        blank=True,
        help_text="Description of Movie"
    )
    image_path = models.CharField(
        max_length=255,
        help_text="Image path of Movie")
    duration = models.IntegerField(
        blank=True,
        help_text="Duration of Movie"
    )
    mpaa_rating = JSONField(
        default=dict,
        help_text="JSON of the Mpaa Rating")
    user_rating = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Relational fields
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(
        'movies.Language',
        null=True,
        on_delete=models.CASCADE,
        help_text="Movie's language")

    class Meta:
        ordering = ['-id']
