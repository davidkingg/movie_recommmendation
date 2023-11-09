import os
import requests
from rest_framework import generics
from rest_framework import generics, permissions

from user_management.models import MyUser
# from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response

@api_view(['GET'])
def MovieDetailView(request, id):
    if not request.user.is_authenticated:
        return Response({"message":"not authorized, please login"})
    url = os.getenv("api_url")
    idd =  id#request.GET.get("id")

    querystring = {"i": f"{idd}", "r": "json"}
    headers = {
        "X-RapidAPI-Key": os.getenv("movie_api_key"),
        "X-RapidAPI-Host": os.getenv("api_host"),
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=200)
    movie = response.json()
    return Response(movie)

@api_view(['GET'])
def MovieListView(request):
    url = os.getenv("api_url")
    title = request.GET.get("title")
    if title is None:
        return Response({"message":"not title provided as query parameter"})
    querystring = {"s": f"{title}", "r": "json", "page": "1"}

    headers = {
        "X-RapidAPI-Key": os.getenv("movie_api_key"),
        "X-RapidAPI-Host": os.getenv("api_host"),
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=200)
    movie = response.json()
    return Response(movie)