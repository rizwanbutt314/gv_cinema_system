from .models import Movies
from rest_framework import serializers


class MoviesSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    def get_language(self, obj):
        return obj.language.title

    def get_genre(self, obj):
        genre_titles = [genre.title for genre in obj.genre_list]
        return genre_titles

    class Meta:
        model = Movies
        fields = ('id', 'name', 'description', 'image_path', 'duration', 'mpaa_rating', 'user_rating',
                  'language', 'genre')
