from django.test import SimpleTestCase
from django.urls import reverse,resolve
from user_management.views import *

class TestUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url =reverse('login')
        print (resolve(url))
        self.assertEqual(resolve(url).func, Login)

    def test_home_url_is_resolved(self):
        url =reverse('home')
        print (resolve(url))
        self.assertEqual(resolve(url).func, home)

    def test_logout_url_is_resolved(self):
        url =reverse('logout')
        print (resolve(url))
        self.assertEqual(resolve(url).func, Logout)

    def test_register_url_is_resolved(self):
        url =reverse('register')
        print (resolve(url))
        self.assertEqual(resolve(url).func, register)

    def test_search_url_is_resolved(self):
        url =reverse('search')
        print (resolve(url))
        self.assertEqual(resolve(url).func, search_movie)

    def test_profile_url_is_resolved(self):
        url =reverse('profile',args=['str'])
        print (resolve(url))
        self.assertEqual(resolve(url).func, profile)

    def test_update_url_is_resolved(self):
        url =reverse('update')
        print (resolve(url))
        self.assertEqual(resolve(url).func, update)

    def test_delete_url_is_resolved(self):
        url =reverse('delete')
        print (resolve(url))
        self.assertEqual(resolve(url).func, delete_user)