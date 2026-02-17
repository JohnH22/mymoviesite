import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Movie, Category, Director
from django.db.models import Q
from .forms import ReviewForm, CustomUserCreationForm
from django.db.models import Avg, F
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

# Helper function for OMDb API
def get_imdb_data(imdb_id):
    api_key = '905975de'
    url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('Response') == 'True' :
            return {
                'rating': data.get('imdbRating'),
                'votes': data.get('imdbVotes'),
            }
    except requests.RequestException:
        pass
    return {'rating': None, 'votes': 'N/A'}


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

# LOGIC FOR IMDB SCORE (DYNAMIC OR MANUAL)
    imdb_data = {'rating': None, 'votes': 'N/A'}

#Try for API if there is ID
    if movie.imdb_id:
        imdb_data = get_imdb_data(movie.imdb_id)

#Final score select
    if imdb_data['rating'] and imdb_data['rating'] != 'N/A':
        final_imdb_score = imdb_data['rating']
    else:
        #Fallback into the old manual insert field if API fails or doesn't exist
        final_imdb_score = movie.imdb_score if movie.imdb_score else "N/A"


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
        'imdb_rating': final_imdb_score,
        'imdb_votes': imdb_data['votes'],
    }
    return render(request, 'movie/movie_detail.html', context)



def about_us(request):
    return render(request, 'movie/about_us.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save user and log them in automatically using the custom case-insensitive backend.
            user = form.save()
            login(request, user, backend='movie.backends.CaseInsensitiveModelBackend')
            return redirect('movie_list')
    else:
        form = CustomUserCreationForm()

        # Defining what each field "shows"
        placeholders = {
            'username': 'Choose a Username',
            'email': 'Enter your Email Address',
            'password1': 'Choose a Password',
            'password2': 'Confirm your Password'
        }

        # For loop to pass all the settings to all the fields
        for field_name, text in placeholders.items():
            form.fields[field_name].widget.attrs.update({
                'class': 'auth-input-style',
                'placeholder': text
            })

        # The Username for the max length setting
        form.fields['username'].help_text = "Requires 20 characters or fewer."
        form.fields['username'].widget.attrs['maxlength'] = 20


    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user, backend='movie.backends.CaseInsensitiveModelBackend')
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
        form.fields['username'].label = "Username or Email Address"
        form.fields['username'].widget.attrs.update({
            'class': 'auth-input-style',
            'placeholder': 'Enter your Username or Email Address'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'auth-input-style',
            'placeholder': 'Enter your Password'
        })

    return render(request, 'registration/login.html', {'form': form})