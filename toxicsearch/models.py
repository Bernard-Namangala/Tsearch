from django.db import models


class Movie(models.Model):
    movie_title = models.CharField(max_length=255)
    movie_link = models.URLField()

    def __str__(self):
        return self.movie_title


class Series(models.Model):
    series_title = models.CharField(max_length=255)
    series_link = models.URLField()

    def __str__(self):
        return self.series_title

    class Meta:
        verbose_name_plural = "Series"