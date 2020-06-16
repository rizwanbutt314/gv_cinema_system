from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status


class MoviesAPIIndexTest(TestCase):
    """
        Make a GET request to endpoint "/api/movies/" to
        1. get all movies data
        2. get movies using search
    """
    fixtures = ['genre.json', 'language.json', 'movies.json']

    def setUp(self):
        self.url = reverse_lazy('movies_api:movies_listing')

    def test_get_all_movies(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['count'], 30)
        self.assertIn("Disney's Zootopia", api_index_data['results'][0]['name'])
        self.assertIn("Criminal", api_index_data['results'][1]['name'])

    def test_get_movies_using_search(self):
        r = self.client.get(self.url, {'search': 'request'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['count'], 2)


class MoviesAPIDetailTests(TestCase):
    """
        Make a GET request to endpoint "/api/movies/<pk>/" to
        1. get movie data using id
    """
    fixtures = ['genre.json', 'language.json', 'movies.json']

    def setUp(self):
        self.unavailable_movie_id = 219
        self.available_movie_id = 34
        self.available_movie_url = reverse_lazy('movies_api:movie_detail', args=(self.available_movie_id,))
        self.unavailable_movie_url = reverse_lazy('movies_api:movie_detail', args=(self.unavailable_movie_id,))

    def test_get_movie(self):
        # get existing movie data using id
        r = self.client.get(self.available_movie_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)

        # get non-exisiting movie data using id
        r = self.client.get(self.unavailable_movie_url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

        api_index_data = r.json()
        self.assertEqual(api_index_data['detail'], 'Not found.')
