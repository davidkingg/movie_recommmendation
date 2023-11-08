from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_user, name="login"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("logout", views.logout_user, name="logout"),
    path("delete", views.delete_user, name="delete"),
    path("update", views.update, name="update"),
    path("register", views.register, name="register"),
]
