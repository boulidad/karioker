from django.db import models
from django.contrib.auth.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.urls import reverse
from karioker.models import Songs
from django.shortcuts import  get_object_or_404


class Event(models.Model):
    name = models.CharField(max_length=100)
    orgenizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_invite_token(self, expires_sec=86400):
        s = Serializer('hf39h4nf3948fn93u8fn39hnvrh30h', expires_sec)
        #s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'event_id': self.id}).decode('utf-8')
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    @staticmethod
    def verify_invite_token(token):
        s = Serializer('hf39h4nf3948fn93u8fn39hnvrh30h')
        try:
            event_id = s.loads(token)['event_id']
        except:
            return None
        return get_object_or_404(Event, id=event_id)

    def __str__(self):
        return self.name


class EventGuests(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.guest.username}@{self.event.name}'

class EventSongs(models.Model):
    singer = models.ForeignKey(EventGuests, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.song} by {self.singer}'


#class SendEventInvitation()

