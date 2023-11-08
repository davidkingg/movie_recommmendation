from django.test import SimpleTestCase
from django.urls import reverse,resolve
from movie_search.views import *


class TestUrls(SimpleTestCase):
    def test_search_url_is_resolved(self):
        url =reverse('search')
        print (resolve(url))
        self.assertEqual(resolve(url).func, search_movie)

    def test_movie_detail_url_is_resolved(self):
        url =reverse('movie_detail')
        print (resolve(url))
        self.assertEqual(resolve(url).func, movie_detail)