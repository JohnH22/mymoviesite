from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie
from django.db.models import Q

def movie_list(request):
    cat = request.GET.get('cat')
    txt = request.GET.get('txt')
    if not cat:
        if txt:
            movies = Movie.objects.filter((Q(text__icontains=txt) | Q(title__icontains=txt)) & Q(published_date__lte=timezone.now())).order_by('published_date')
        else:
            movies = Movie.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    elif cat.isdigit():
        cat=int(cat)
        movies = Movie.objects.filter(published_date__lte=timezone.now()).filter(category=cat).order_by('published_date')
    else:
        movies = Movie.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'movie/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie/movie_detail.html', {'movie': movie})

def about_us(request):
    return render(request, 'movie/about_us.html')