from django.shortcuts import render, redirect
from .forms import SearchForm

from .models import Movie, Series
from .tasks import Thread
from .scrape import should_be_added


def index_view(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
    else:
        form = SearchForm
        context = {
            'form': form
        }
    return render(request=request, template_name='toxicsearch/index.html', context=context)


def search_view(request):
    if request.method == "POST":
        movies_in_db = Movie.objects.all()
        series_in_db = Series.objects.all()
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            movies = []
            series = []
            for movie in movies_in_db:
                if should_be_added(search, movie.movie_title):
                    movies.append(movie)
            for serie in series_in_db:
                if should_be_added(search, serie.series_title):
                    series.append(serie)
    else:
        form = SearchForm
        movies = []
        series = []
    context = {
        'form': form,
        'movies': movies,
        'series': series
    }
    return render(request=request, template_name='toxicsearch/results.html', context=context)


def update_db(request):
    thread_for_movies = Thread()
    thread_for_series = Thread()
    thread_for_movies.start()
    thread_for_series.start()
    thread_for_series.add_series_to_database()
    thread_for_movies.add_series_to_database()
    return redirect('/')


def update_movies_table(request):
    thread = Thread()
    thread.start()
    thread.add_movies_to_database()
    return redirect('/')


def update_series_table(request):
    thread = Thread()
    thread.start()
    thread.add_series_to_database()
    return redirect('/')


def handler404(request, exception):
    return render(request=request, template_name='404.html')
