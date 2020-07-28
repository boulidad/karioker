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
    language = models.CharField(max_length=400) 
    alignment = models.CharField(max_length=400) 


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


def get_create_composer(composer_name):
    try:
        composer=Composers.objects.get(name=composer_name)
    except Composers.DoesNotExist:
        composer=Composers(name=composer_name)
        composer.save()
    return composer

def get_create_performer(performer_name):
    try:
        performer=Performers.objects.get(name=performer_name)
    except Performers.DoesNotExist:
        performer=Performers(name=performer_name)
        performer.save()
    return performer

def get_create_song_writer(song_writer_name):
    try:
        song_writer=SongWriters.objects.get(name=song_writer_name)
    except SongWriters.DoesNotExist:
        song_writer=SongWriters(name=song_writer_name)
        song_writer.save()
    return song_writer


def get_create_song(song_dict):
    try:
        song=Songs.objects.get(lyrics_url=song_dict['lyrics_url'])
        return {'song':song,'status':'song_already_exists'}
    except Songs.DoesNotExist:
        performer=get_create_performer(performer_name=song_dict['performer'])
        song_writer=get_create_song_writer(song_writer_name=song_dict['song_writer'])
        composer=get_create_composer(composer_name=song_dict['composer'])
        song=Songs(name=song_dict['title'],
            performer=performer,
            songwriter=song_writer,
            composer=composer,
            lyrics_url=song_dict['lyrics_url'],
            chords_url=song_dict['chords_url'],
            lyrics=song_dict['lyrics'],
            chords=song_dict['chords'],
            alignment=song_dict['alignment'],
            language=song_dict['language']
            )

        song.save()
        return {'song':song,'status':'new_song_created'}



