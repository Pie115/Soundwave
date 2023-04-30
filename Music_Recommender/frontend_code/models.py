from django.db import models

# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=100)
