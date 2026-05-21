from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title