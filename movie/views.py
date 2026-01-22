from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie

def movie_list(request):
    cat = request.GET.get('cat', '').strip()
    if cat == '':
        movies = Movie.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    else:
        cat = int(cat)
        movies = Movie.objects.filter(published_date__lte=timezone.now()).filter(category=cat).order_by('published_date')
    return render(request, 'movie/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie/movie_detail.html', {'movie': movie})
