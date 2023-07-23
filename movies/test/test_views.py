from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import User, Movie, Review
from ..views import RegistserView, LoginView, GetMoviesView, MovieView, ReviewView, RatingView

import jwt,datetime

class RegisterViewTestCase(TestCase):
    def test_user_registration_successful(self):
        client = APIClient()
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpassword', 'name': 'Test User', 'email': 'testuser@example.com'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_missing_username(self):
        client = APIClient()
        url = reverse('register')
        data = {'password': 'testpassword', 'name': 'Test User', 'email': 'testuser@example.com'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_missing_password(self):
        client = APIClient()
        url = reverse('register')
        data = {'username': 'testuser', 'name': 'Test User', 'email': 'testuser@example.com'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_missing_name(self):
        client = APIClient()
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'testuser@example.com'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', name='Test User', email='testuser@example.com')

    def test_user_login_successful(self):
        client = APIClient()
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        # Add more assertions based on your expected data

    def test_user_login_invalid_password(self):
        client = APIClient()
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_invalid_username(self):
        client = APIClient()
        url = reverse('login')
        data = {'username': 'nonexistentuser', 'password': 'testpassword'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetMoviesViewTestCase(TestCase):
    def test_get_movies_successful(self):
        client = APIClient()
        url = reverse('getmovies')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieViewTestCase(TestCase):
    def setUp(self):
        self.movie1 = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12345',
            original_language = 'en',
            original_title = 'Movie with Rating',
            release_date = '2023-07-22',
            vote_average=8.5,
            video = False
        )
        self.movie2 = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12346',
            original_language = 'en',
            original_title = 'Movie without Rating',
            release_date = '2023-07-22',
            video = False
        )

    def get_authenticated_client(self,user):
        # Helper method to create an authenticated client
        client = APIClient()
        token = self.generate_jwt_token(user)
        # Set the token as a cookie in the test client
        client.cookies['jwt'] = token
        return client

    def generate_jwt_token(self, user):
        # Helper method to manually generate JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_movies_authenticated(self):
        # A new user for this test case
        user = User.objects.create_user(username='testuser1', password='testpassword1', name='Test User 1', email='testuser1@example.com')

        client = self.get_authenticated_client(user)
        url = reverse('movielist')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_movies_unauthenticated(self):
        client = APIClient()
        url = reverse('movielist')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_movie_details_authenticated(self):
        # A new user for this test case
        user = User.objects.create_user(username='testuser2', password='testpassword2', name='Test User 2', email='testuser2@example.com')

        client = self.get_authenticated_client(user)
        url = reverse('movielist')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class ReviewViewTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12345',
            original_language = 'en',
            original_title = 'Movie with Rating',
            release_date = '2023-07-22',
            vote_average=8.5,
            video = False
        )

    def get_authenticated_client(self,user):
        # Helper method to create an authenticated client
        client = APIClient()
        token = self.generate_jwt_token(user)
        # Set the token as a cookie in the test client
        client.cookies['jwt'] = token
        return client

    def generate_jwt_token(self, user):
        # Helper method to manually generate JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_post_review_authenticated(self):
        # A new user for this test case
        user = User.objects.create_user(username='testuser1', password='testpassword1', name='Test User 1', email='testuser1@example.com')

        client = self.get_authenticated_client(user)

        url = reverse('review')
        data = {'local_movie_id': self.movie.id, 'content': 'This is a test review.'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)

    def test_post_review_unauthenticated(self):
        client = APIClient()
        url = reverse('review')
        data = {'local_movie_id': self.movie.id, 'content': 'This is a test review.'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.count(), 0)

# Add test cases for RatingView
class RatingViewTestCase(TestCase):
    def setUp(self):
        # Create movies with and without ratings
        self.movie_with_rating = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12345',
            original_language = 'en',
            original_title = 'Movie with Rating',
            release_date = '2023-07-22',
            vote_average=8.5,
            video = False
        )
        self.movie_without_rating = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12346',
            original_language = 'en',
            original_title = 'Movie without Rating',
            release_date = '2023-07-22',
            video = False
        )

    def test_get_average_rating(self):
        client = APIClient()
        url = reverse('ratings')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

        movie_with_rating = next(movie for movie in response.data if movie['original_title'] == 'Movie with Rating')
        self.assertEqual(movie_with_rating['rating'], 8.5)

        movie_without_rating = next(movie for movie in response.data if movie['original_title'] == 'Movie without Rating')
        self.assertEqual(movie_without_rating['rating'], "NA")