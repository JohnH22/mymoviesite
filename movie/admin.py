from django.contrib import admin
from .models import Movie, Category, Director, Review

# Register your models here.
admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(Director)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user_review', 'rating_review', 'posted_review')
    list_filter = ('rating_review', 'posted_review', 'movie')
    search_fields = ('comment_review', 'user_review__username', 'movie__title')