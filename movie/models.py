from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey('Category' , null=True, on_delete=models.CASCADE)
    director = models.ForeignKey('Director', null=True, on_delete=models.CASCADE )
    image = models.ImageField(upload_to='movies/%Y/%m/', null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in minutes")
    trailer_url = models.URLField(max_length=200, null=True, blank=True, help_text="Youtube Link (e.g., https://www.youtube.com/watch?v=...)" )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    user_review = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_review = models.TextField()
    rating_review = models.PositiveSmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)])
    posted_review = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user_review.username}"