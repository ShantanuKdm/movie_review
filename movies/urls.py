from django.urls import path
from .views import MovieView, RatingView, RegistserView, LoginView, GetMoviesView, ReviewView

urlpatterns = [
    path("register", RegistserView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("getmovies", GetMoviesView.as_view(), name="getmovies"),
    path("movielist", MovieView.as_view(), name="movielist"),
    path("review", ReviewView.as_view(), name="review"),
    path("ratings", RatingView.as_view(), name="ratings")
]
