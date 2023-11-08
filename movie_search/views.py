import os
import requests
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv


load_dotenv()


@login_required(login_url="/login")
def movie_detail(request):
    """fetches a movie. the imdb ID if the movie must be provided"""
    
    if request.method == "POST":
        url = os.getenv("api_url")
        idd = request.POST["id"]
        year = request.POST["year"]
        plot = request.POST["plot"]

        querystring = {"i": f"{idd}", "r": "json", "y": year, "plot": plot}
        headers = {
            "X-RapidAPI-Key": os.getenv("movie_api_key"),
            "X-RapidAPI-Host": os.getenv("api_host"),
        }
        response = requests.get(url, headers=headers, params=querystring, timeout=200)
        # return JsonResponse( response.json())
        return render(request, "movie_list.html", {"response": response.json()})
    else:
        return render(request, "movie.html")


@login_required(login_url="/login")
def search_movie(request):
    """searches for a movie with the title alone and returns multiple match where possible"""

    url = os.getenv("api_url")
    title = request.GET["title"]
    querystring = {"s": f"{title}", "r": "json", "page": "1"}
    headers = {
        "X-RapidAPI-Key": os.getenv("movie_api_key"),
        "X-RapidAPI-Host": os.getenv("api_host"),
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=200)
    # return JsonResponse( response.json()["Search"], safe=False)
    if "Search" in response.json():
        return render(
            request,
            "movie_list.html",
            {"response": response.json()["Search"], "page": "list"},
        )
    return HttpResponse("No movie found")
