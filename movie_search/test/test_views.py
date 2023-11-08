from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import MyUser


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse("search")
        self.search_detail_url = reverse("movie_detail")
        self.new_user = MyUser.objects.create(email="test@gmail.com", password="1234")

    def test_movie_search(self):
        ''' test movie search page function '''
        self.client.force_login(self.new_user)
        response = self.client.get(
            self.search_url+'?title=avengers')
        self.assertEquals(response.status_code, 200)

    def test_smovie_detail_search(self):
        ''' test movie search page function '''
        self.client.force_login(self.new_user)
        response = self.client.post(
            self.search_detail_url, {"id": "tt0848228", "year":"2019", "plot":"short"})
        self.assertEquals(response.status_code, 200)