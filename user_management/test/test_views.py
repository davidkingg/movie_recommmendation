from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import MyUser


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.register_url = reverse("register")
        self.search_url = reverse("search")
        self.new_user = MyUser.objects.create(email="test@gmail.com", password="1234")
        self.profile_url = reverse("profile", args=[self.new_user.id])
        self.delete_url = reverse("delete")

    def test_home(self):
        ''' test homepage function '''
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/home.html")

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/login_page.html")

    def test_login_post(self):
        ''' test loginpage function '''
        response = self.client.post(
            self.login_url, {"email": self.new_user.email, "password": self.new_user.password}
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/login_page.html")

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/signup.html")

    def test_register_post(self):
        ''' test registration page function '''
        response = self.client.post(
            self.register_url, {"username": "king", "password": 1122}
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/signup.html")

    def test_profile(self):
        ''' test user profile page function '''
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_management/profile.html")

    def test_delete_user_get(self):
        response = self.client.get(self.delete_url)
        self.assertEquals(response.status_code, 200)

    def test_delete_user_post(self):
        ''' test delete user page function '''
        self.client.force_login(self.new_user)
        response = self.client.post(
            self.delete_url, {"email": f"{self.new_user.email}"})
        deleted = MyUser.objects.filter(email=self.new_user.email).exists()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(deleted, False)

