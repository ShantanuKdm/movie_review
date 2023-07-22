import requests, datetime
import jwt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import Review, User, Movie

# Create your views here.


class RegistserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"token": token}
        return response


class GetMoviesView(APIView):
    def get(self, request):
        import requests

        url = "https://api.themoviedb.org/3/discover/movie"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYTQxZmYwOTYzNDJlMjdhYTk2YjQxNjcwYjRjNjY2ZCIsInN1YiI6IjY0YmJlMzY5MGVkMmFiMDEzOGY3ZmMyZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mEi7yydQG0ZivfsMv2H0jEaJcxj-zu_Tf1bLxTw6oBA",
        }

        response = requests.get(url, headers=headers)

        for movie in response.json().get("results", []):
            movie_id = movie.pop("id")
            movie["movie_id"] = movie_id
            _movie, _ = Movie.objects.update_or_create(movie_id=movie_id, defaults=movie)
            url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"

            review_response = requests.get(url, headers=headers)
            for review in review_response.json().get("results", []):
                review_id = review.pop("id")
                review_created_at = review.pop("created_at")
                review_updated_at = review.pop("updated_at")
                review["review_id"] = review_id
                review["review_created_at"] = review_created_at
                review["review_updated_at"] = review_updated_at
                review["movie_id"] = _movie.id
                Review.objects.update_or_create(review_id = review_id,defaults=review)

        return Response({"success: True"})
