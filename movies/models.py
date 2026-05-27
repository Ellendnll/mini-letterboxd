from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    tmdb_id = models.IntegerField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    

    overview = models.TextField(blank=True, null=True)
    release_date = models.CharField(max_length=20, blank=True, null=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True) 

    def __str__(self):
        return self.title