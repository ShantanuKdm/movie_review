import requests, datetime
import jwt

from rest_framework import status
from django.db.models import F
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import MovieSerializer, UserSerializer
from .models import Review, User, Movie
from rest_framework.exceptions import APIException


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Incorrect authentication credentials.'
    default_code = 'authentication_failed'

#user registration
class RegistserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

#user login
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

#initial movie and review data seeding Api
class GetMoviesView(APIView):

    def get(self, request):
        try:
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
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#fetch movies list if authenticated
class MovieView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data)

#open endpoint to get average rating
class RatingView(APIView):

    def get(self, request):
        movies = Movie.objects.all().values('original_title',rating=F('vote_average'))
        for movie in movies:
            if not movie.get('rating'):
                movie['rating'] = "NA"
        return Response(movies)

# post review if authenticated
class ReviewView(APIView):

    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        user_details = {
                "name" : user.name,
                "username" : user.username,
            }

        movie = Movie.objects.filter(id = request.data['local_movie_id']).first()
        if not movie:
            raise Exception('Movie does not exist')

        Review.objects.create(
            author = user.name,
            author_details = user_details,
            content = request.data['content'],
            review_created_at = datetime.datetime.utcnow(),
            review_id = None,
            movie = movie,
            review_updated_at = datetime.datetime.utcnow(),
            url = None
        )
        return Response({"success: True"})
        