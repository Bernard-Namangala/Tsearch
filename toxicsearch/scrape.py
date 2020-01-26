import requests
from bs4 import BeautifulSoup
import re
from difflib import SequenceMatcher
import jellyfish
import os
import time


def get_largest_page(soup):
    """
    function to return the number of the newest page on toxic wap
    :param soup:
    :return:
    """
    assert isinstance(soup, BeautifulSoup)
    next_a = soup.findAll('li')[-1]
    last_a = next_a.find('a').get('href')
    largest_page = re.search(r'\d+', last_a)[0]
    return largest_page


def extract_movie_and_link(soup):
    assert isinstance(soup, BeautifulSoup)
    links_to_movies = soup.findAll('li')
    movies = []
    for link_to_movie in links_to_movies:
        movie_title = link_to_movie.text
        link = link_to_movie.find('a').get('href')
        complete = (movie_title, link)
        movies.append(complete)
    return movies


def get_movies_on_page(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    movies = extract_movie_and_link(soup)
    return movies


def get_all_movies():
    site = "http://toxicwap.com/New_Movies/"
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    largest_page = int(get_largest_page(soup))
    movies = get_movies_on_page(site)
    if movies:
        movies.pop()
        go_on = True
    else:
        go_on = False

    while go_on:
        site = f"http://toxicwap.com/New_Movies/00{str(largest_page)}.php"
        movies_on_page = get_movies_on_page(site)
        if movies_on_page:
            movies_on_page.pop()
            movies += movies_on_page
            largest_page -= 1
        else:
            go_on = False
    return movies


def get_similar_movies(string):
    then = time.time()
    alike_movies = []
    for movie in get_all_movies():
        match_ratio = jellyfish.jaro_winkler(str(movie[0][:-4]).lower(), string.lower())
        if (str(string).lower() in str(movie[0][:-4]).lower() and match_ratio > 0.4) or match_ratio >= 7.4:
            alike_movies.append((movie, match_ratio))

    alike_movies = sorted(alike_movies, key=lambda x: x[-1])
    now = time.time()  # Time after it finished
    print("It took: ", now - then, " seconds")
    return alike_movies


def should_be_added(string, movie):
    match_ratio = jellyfish.jaro_winkler(str(movie[:-4]).lower(), string.lower())
    if (str(string).lower() in str(movie[:-4]).lower() and match_ratio > 0.4) or match_ratio >= 7.4:
        return True
    else:
        return False


def get_all_similar_movies(string):
    site = "http://toxicwap.com/New_Movies/"
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    largest_page = int(get_largest_page(soup))
    first_page_movies = get_movies_on_page(site)
    moviez = []
    for movie in first_page_movies:
        if should_be_added(string, movie):
            moviez.append(movie)
    go_on = True
    while go_on:
        site = f"http://toxicwap.com/New_Movies/00{str(largest_page)}.php"
        movies = get_movies_on_page(site)
        if movies:
            for movie in movies:
                if should_be_added(string, movie):
                    moviez.append((movie))
                    print(type(movie))
            largest_page -= 1
        else:
            go_on = False
    return moviez


def get_series_on_page(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    series = soup.findAll('li')
    if series:
        series.pop(-1)
    all_series = []
    for serie in series:
        serie_title = serie.text
        serie_link = serie.find('a').get('href')
        full_serie = (serie_title, serie_link)
        all_series.append(full_serie)
    if series:
        return True, all_series
    return False, all_series


def get_all_series_for_specific_letter(letter):
    url = 'http://toxicwap.com/TV_Series/{}.php'.format(letter)
    all_series = []
    current_series = get_series_on_page(url=url)
    counter = 1
    if current_series[0]:
        go_on = True
        if current_series[-1]:
            all_series.extend(current_series[-1])
    else:
        go_on = False

    while go_on:
        counter += 1
        prefix = '0'
        if counter > 9:
            prefix = ''
        formatter = "{}{}".format(prefix, counter)
        url = "http://toxicwap.com/TV_Series/{}{}.php".format(letter, formatter)
        current_series = get_series_on_page(url)
        if current_series[0]:
            if current_series[-1]:
                all_series.extend(current_series[-1])
        else:
            go_on = False
    return all_series


def get_all_series():
    letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'
               , 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    all_series = []

    for letter in letters:
        series_for_letter = get_all_series_for_specific_letter(letter)
        all_series.extend(series_for_letter)

    # get cartoons
    cartoons = get_all_series_for_specific_letter('cartoons/_all')
    all_series.extend(cartoons)

    return all_series



