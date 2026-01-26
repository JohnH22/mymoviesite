from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie, Category, Director
from django.db.models import Q

def movie_list(request):
    cat = request.GET.get('cat', '')
    txt = request.GET.get('txt', '')
    dir = request.GET.get('dir', '')

    movies = Movie.objects.all().order_by('-published_date')



    if txt:
            movies = movies.filter(Q(text__icontains=txt) | Q(title__icontains=txt))

    if cat and cat.isdigit():
            movies = movies.filter(category_id=int(cat))

    if dir and dir.isdigit():
            movies = movies.filter(director_id=int(dir))

    return render(request, 'movie/movie_list.html', {'movies': movies, 'categories': Category.objects.all(), 'directors': Director.objects.all()})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie/movie_detail.html', {'movie': movie})

def about_us(request):
    return render(request, 'movie/about_us.html')