from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class SongWriters(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Composers(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Performers(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Songs(models.Model):
	name = models.CharField(max_length=100)
	performer = models.ForeignKey(Performers, on_delete=models.CASCADE)
	songwriter = models.ForeignKey(SongWriters, on_delete=models.CASCADE)
	composer = models.ForeignKey(Composers, on_delete=models.CASCADE)
	lyrics_url = models.CharField(max_length=400) 
	chords_url = models.CharField(max_length=400)
	lyrics = models.TextField()
	chords = models.TextField()

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('song-detail', kwargs={'pk': self.pk})


class Parties(models.Model):
	name = models.CharField(max_length=100)
	orgenizer = models.ForeignKey(User, on_delete=models.CASCADE)

class Party_Song_Lists(models.Model):
	party = models.ForeignKey(Parties, on_delete=models.CASCADE)
	Song = models.ForeignKey(Songs, on_delete=models.CASCADE)

