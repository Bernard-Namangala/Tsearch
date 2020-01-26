from .models import Movie, Series
from .scrape import get_all_movies, get_all_series
import threading


def add_movies_to_database():
    movies_in_db = Movie.objects.all()
    movies_to_add = list(get_all_movies())
    for movie in movies_to_add:
        add = True
        for movie_in_db in movies_in_db:
            if movie[-1] == movie_in_db.movie_link:
                add = False
        if add:
            Movie.objects.create(movie_title=movie[0], movie_link=movie[-1])
        else:
            movies_to_add.remove(movie)


def add_series_to_database():
    series_in_db = Series.objects.all()
    series_to_add = list(get_all_series())
    for series in series_to_add:
        add = True
        for serie_in_db in series_in_db:
            if series[-1] == serie_in_db.series_link:
                add = False
        if add:
            Series.objects.create(series_title=series[0], series_link=series[-1])
        else:
            series_to_add.remove(series)


class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def add_movies_to_database():
        movies_in_db = Movie.objects.all()
        movies_to_add = list(get_all_movies())
        for movie in movies_to_add:
            add = True
            for movie_in_db in movies_in_db:
                if movie[-1] == movie_in_db.movie_link:
                    add = False
            if add:
                Movie.objects.create(movie_title=movie[0], movie_link=movie[-1])
            else:
                movies_to_add.remove(movie)

    @staticmethod
    def add_series_to_database():
        series_in_db = Series.objects.all()
        series_to_add = list(get_all_series())
        for series in series_to_add:
            add = True
            for serie_in_db in series_in_db:
                if series[-1] == serie_in_db.series_link:
                    add = False
            if add:
                Series.objects.create(series_title=series[0], series_link=series[-1])
            else:
                series_to_add.remove(series)