from django.urls import path
from . import views

urlpatterns = [
    path("search", views.search_movie, name="search"),
    path("movie_detail", views.movie_detail, name="movie_detail"),
]
