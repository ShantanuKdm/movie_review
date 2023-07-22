from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "User"


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=255)
    genre_ids = models.JSONField()
    movie_id = models.CharField(max_length=255, unique=True)
    original_language = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.DecimalField(decimal_places=2, max_digits=6)
    poster_path = models.CharField(max_length=255)
    release_date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    video = models.BooleanField()
    vote_average = models.DecimalField(decimal_places=2, max_digits=6)
    vote_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Movie"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255)
    author_details = models.JSONField()
    content = models.TextField()
    review_created_at = models.DateTimeField()
    review_id = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_updated_at = models.DateTimeField()
    url = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Review"
