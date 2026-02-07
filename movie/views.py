from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Movie, Category, Director
from django.db.models import Q
from .forms import ReviewForm
from django.db.models import Avg, F
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def movie_list(request):
    cat = request.GET.get('cat', '')
    txt = request.GET.get('txt', '')
    dir = request.GET.get('dir', '')

    movies = Movie.objects.filter(published_date__lte=timezone.now()).annotate(
        avg_raw=Avg('reviews__rating_review')
    ).order_by('-release_date')



    if txt:
            movies = movies.filter(Q(text__icontains=txt) | Q(title__icontains=txt))

    if cat and cat.isdigit():
            movies = movies.filter(category_id=int(cat))

    if dir and dir.isdigit():
            movies = movies.filter(director_id=int(dir))

    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for movie in page_obj:
        if movie.avg_raw:
            movie.display_rating = movie.avg_raw * 2
        else:
            movie.display_rating = None


    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'directors': Director.objects.all(),
        'current_cat': cat,
        'current_txt': txt,
        'current_dir': dir,
    }

    return render(request, 'movie/movie_list.html', context)



def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    reviews = movie.reviews.all().order_by('-posted_review')

    average_rating = reviews.aggregate(Avg('rating_review'))['rating_review__avg']

    if average_rating:
        average_rating = average_rating * 2

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.user_review = request.user
                review.save()
                messages.success(request, "Your review has been posted successfully!")
                return redirect('movie_detail', pk=pk)
        else:
            form = redirect('login')
    else:
        form = ReviewForm()

    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
    }
    return render(request, 'movie/movie_detail.html', context)



def about_us(request):
    return render(request, 'movie/about_us.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save user and log them in automatically using the custom case-insensitive backend.
            user = form.save()
            login(request, user, backend='movie.backends.CaseInsensitiveModelBackend')
            return redirect('movie_list')
    else:
        form = UserCreationForm()
        form.fields['username'].help_text = "Required. 20 characters or fewer."
        form.fields['username'].widget.attrs['maxlength']= 20
        # UI: Customize form fields with placeholders and specific constraints.
        form.fields['username'].widget.attrs['placeholder']= "Choose a Username"
        form.fields['password1'].widget.attrs['placeholder']= "Choose a Password"
        form.fields['password2'].widget.attrs['placeholder'] = "Confirm your Password"


    return render(request, 'registration/register.html', {'form': form})
