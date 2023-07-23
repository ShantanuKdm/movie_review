from django.test import TestCase

from ..models import User, Movie, Review
# Create your tests here.

class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword', name='Test User', email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))

class MovieModelTestCase(TestCase):
    def test_movie_creation(self):
        movie_data = {
            'adult': True,
            'backdrop_path': '/path/to/backdrop.jpg',
            'genre_ids': [12, 28, 80],
            'movie_id': '12345',
            'original_language': 'en',
            'original_title': 'Test Movie',
            'overview': 'This is a test movie.',
            'popularity': 123.45,
            'poster_path': '/path/to/poster.jpg',
            'release_date': '2023-07-22',
            'title': 'Test Movie',
            'video': False,
            'vote_average': 7.8,
            'vote_count': 100,
        }
        movie = Movie.objects.create(**movie_data)
        for key, value in movie_data.items():
            self.assertEqual(getattr(movie, key), value)
    

class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            adult = True,
            backdrop_path = '/path/to/backdrop.jpg',
            genre_ids = [12, 28, 80],
            movie_id = '12345',
            original_language = 'en',
            original_title = 'Test Movie',
            release_date = '2023-07-22',
            video = False
        )
    
    def test_review_creation(self):
        review_data = {
            'author': 'Test Author',
            'author_details': {'name': 'Test Author'},
            'content': 'This is a test review.',
            'review_created_at': '2023-07-22T12:00:00Z',
            'review_id': 'abc123',
            'movie': self.movie,
            'review_updated_at': '2023-07-22T14:00:00Z',
            'url': '/reviews/abc123',
        }
        review = Review.objects.create(**review_data)
        for key, value in review_data.items():
            self.assertEqual(getattr(review, key), value)