from django.urls import path
from .views import RegistserView, LoginView, GetMoviesView

urlpatterns = [
    path("register", RegistserView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("getmovies", GetMoviesView.as_view(), name="getmovies"),
]
