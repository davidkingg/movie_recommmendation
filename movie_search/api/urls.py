from django.urls import path
from .views import MovieDetailView, MovieListView

urlpatterns = [
    path("movie_detail/<str:id>", MovieDetailView, name="api_movie_detail"),
    path("movie_list", MovieListView, name="api_movie_list"),
]