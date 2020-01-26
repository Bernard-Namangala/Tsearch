from django.urls import path
from . import views

app_name = 'toxicsearch'
urlpatterns = [
    path('', views.index_view, name="home"),
    path('search/', views.search_view, name='search'),
    path('updatedb', views.update_db, name="updatedb"),
    path('update_movies/', views.update_movies_table, name="movies_update"),
    path('update_series/', views.update_series_table, name="series_update"),
]

handler404 = 'toxicsearch.views.handler404'
import toxicsearch.scheduler  # NOQA @isort:skip
import logging
logging.basicConfig(level="DEBUG")
