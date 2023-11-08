import os
import requests
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

from .forms import UserEdit
from .models import MyUser

load_dotenv()


# Create your views here.
def home(request):
    """home page function: returns the homepage template"""
    return render(request, "user_management/home.html")


def login_user(request):
    """Authenticates a user using the email address and password"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        if MyUser.objects.filter(email=email).exists() is True:
            user = MyUser.objects.get(email=email)
        else:
            messages.error(request, "Invalid user")
            return render(request, "user_management/login_page.html")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "password is incorrect")
            return render(request, "user_management/login_page.html")
        else:
            login(request, user)
            return redirect("home")

    return render(request, "user_management/login_page.html")


def profile(request, pk):
    """renders the profile page of a user using the userID as a query parameter"""
    user = MyUser.objects.get(id=pk)
    return render(request, "user_management/profile.html", {"user": user})


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
        response = requests.get(url, headers=headers,
                                params=querystring, timeout=200)
        # return JsonResponse( response.json())
        return render(
            request, "user_management/movie_list.html", {
                "response": response.json()}
        )
    else:
        return render(request, "user_management/movie.html")


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
    response = requests.get(url, headers=headers,
                            params=querystring, timeout=200)
    # return JsonResponse( response.json()["Search"], safe=False)
    if "Search" in response.json():
        return render(
            request,
            "user_management/movie_list.html",
            {"response": response.json()["Search"], "page": "list"},
        )
    return HttpResponse("No movie found")


def logout_user(request):
    """logs out a user"""
    logout(request)
    return redirect("home")


def register(request):
    """creates a user with a uniqe email address"""
    if request.user.is_authenticated:
        return redirect("home")
    page = "register"
    if request.method == "POST":
        pw = request.POST.get("password")
        pw2 = request.POST.get("confirm_password")
        if pw != pw2:
            messages.error(request, "password mismatch")
            return render(request, "user_management/signup.html", {"page": page})
        if MyUser.objects.filter(email=request.POST.get("email")).exists() is True:
            messages.error(request, "email already exists")
            return render(request, "user_management/signup.html", {"page": page})

        userform = MyUser.objects.create_user(
            email=request.POST.get("email").lower(),
            password=request.POST.get("password"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
        )
        # if userform.is_valid():
        userform.save()

        messages.success(request, "Account successfully created")
        return redirect("login")

    return render(request, "user_management/signup.html", {"page": page})


@login_required(login_url="/login")
def update(request):
    """updates a user information like profile picture and name"""
    if request.method == "POST":
        form = UserEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.FILES.get("image", None) is not None:
                try:
                    os.remove(request.user.image.url)
                except Exception as e:
                    print("Exception in removing old profile image: ", e)
                request.user.image = request.FILES["image"]
            request.user.save()
            return redirect("home")
    else:
        form = UserEdit(instance=request.user)
        return render(request, "user_management/update.html", {"form": form})


def delete_user(request):
    """deletes a user"""
    if request.method == "POST":
        idd = request.POST["email"]
        u = MyUser.objects.get(email=request.user.email)
        if idd == u.email:
            u.delete()
            messages.success(request, "The user is deleted")
            return render(request, "user_management/home.html")
        else:
            messages.success(request, "Email does not match registered email")
            return render(request, "user_management/delete.html")
    else:
        return render(request, "user_management/delete.html")
