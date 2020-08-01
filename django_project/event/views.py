from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from karioker.models import Songs
from django.contrib import messages



class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    paginate_by=20

class EventDetailView(DetailView):
    model = Event


class EventSongsListView(ListView):
    model = Event
    context_object_name = 'events'
    paginate_by=500

class KafkaConnect(LoginRequiredMixin,ListView):
    template_name='event/kafka-connect.html'
    model = Event

@login_required
def event_with_details(request,pk):
    event = Event.objects.get(id=pk)
    event_invitation_token=event.get_invite_token()
    guest_list = EventGuests.objects.filter(event=event.id)
    event_song_list = EventSongs.objects.none()
    event_song_list |= EventSongs.objects.filter(event=event.id).order_by('id')

    context = {'event': event, 'guest_list': guest_list,"event_song_list" :event_song_list, 'event_invitation_token':event_invitation_token}
    return render(request, 'event/event_detailed.html', context)

def kafka_connect(request):
    return render(request, 'event/kafka-connect.html')


def home(request):
    context = {
        'songs' : Songs.objects.all()
    }
    return render(request,'karioker/home.html',context)


class AddEventGuest(LoginRequiredMixin,CreateView):
    model = EventGuests
    fields = ['guest']
    success_url = f'/event/'
    def form_valid(self, form):
        form.instance.event = get_object_or_404(Event, id=self.kwargs.get('event_id'))
        return super().form_valid(form)
    #def get_absolute_url(self):
    #    print( f'the event id is {self.event.id}' )
    #    return reverse('event-detail', kwargs={'event_id': self.event.id})

@login_required
def join_event(request,event_id,token):
    #event = get_object_or_404(Event, id=event_id)
    event=Event.verify_invite_token(token)
    print(f'the first  event {event}, {type(event).__name__}')
    if event is None:
        context={'username':request.user.username}
        return render(request, 'event/no_such_event_exists.html',context)
    guest = get_object_or_404(User, id=request.user.id)
    try:
        event_guest = get_object_or_404(EventGuests,event=event,guest=request.user.id)
        messages.success(request,f'you are already a member of this event!')
        print(f'you are already a member of the event {event_guest}')
        return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)
    except:
        event_guest = EventGuests(event=event,guest=guest)
        event_guest.save()
        messages.success(request,f'you have joined the party!')
        return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def event_add_song(request,event_id,song_id):
    song = get_object_or_404(Songs, id=song_id)
    event = get_object_or_404(Event, id=event_id)
    print(song)
    print(f'song_id=s{song_id}')
    print(f'event_id={event_id}')
    print(f'the event object={event}')
    event_guest = get_object_or_404(EventGuests,event=event,guest=request.user.id)
    print(f'event_guest={event_guest}')
    event_guest_song = EventSongs(singer=event_guest,song=song, event=event)

    event_guest_song.save()

    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def event_delete_song(request,event_song_id):
    event_song = get_object_or_404(EventSongs, id=event_song_id)
    event_id=event_song.singer.event.id
    event_song.delete()

    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def start_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    event.event_status = EventStatus.ACTIVE
    event.current_song = EventSongs.objects.filter(event=event_id).order_by('id').first().id
    event_song=EventSongs.objects.get(id=event.current_song)
    event_song.status='CURRENT'

    #next_id = User.objects.order_by('-id').first().id + 1
    #next_id = EventSongs.objects.filter(event=event_id).order_by('id').first().id

    event.save()
    event_song.save()
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def cancel_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    event.event_status = EventStatus.CANCELED
    event.current_song = -1
    event.save()
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def end_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    event.event_status = EventStatus.AFTER
    event.current_song = -1
    for song in EventSongs.objects.filter(event=event_id):
        song.status='LISTED'
        song.save()


    event.save()
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def reset_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    event.event_status = EventStatus.BEFORE
    event.current_song = -1
    event.save()
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def event_next_song(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    current_song=EventSongs.objects.get(id=event.current_song)
    current_song.status='SANG'
    current_song.save()
    try:
        event.current_song = EventSongs.objects.filter(event=event_id,status='LISTED').order_by('id').first().id
        event_song=EventSongs.objects.get(id=event.current_song)
        event_song.status='CURRENT'
        current_song.save()
        event_song.save()
        event.save()
        return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)
    except AttributeError:  # this means that cant get any more songs from the DB, except might be too wide, may need to refactor
        messages.info(request,f'this was the last song     :-(')
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)

@login_required
def event_jump_to_song(request,event_id,event_song_id):
    event = get_object_or_404(Event, id=event_id)
    current_song=EventSongs.objects.get(id=event.current_song)
    current_song.status='SANG'
    current_song.save()
    try:
        event_song=get_object_or_404(EventSongs, id=event_song_id)
        event.current_song = event_song.id
        event_song.status='CURRENT'
        event_song.save()
        event.save()
        return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)
    except AttributeError:  # this means that cant get any more songs from the DB, except might be too wide, may need to refactor
        messages.info(request,f'this was the last song     :-(')
    return redirect(reverse('event-detail', kwargs={'pk': event_id}))#, event_id=event_id)


class EventCreateView(LoginRequiredMixin,CreateView):
    model = Event
    fields = ['name']

    def form_valid(self, form):
        form.instance.orgenizer = self.request.user
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Event
    success_url = '/event/'
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.orgenizer:
            return True
        return False


class EventUpdateView(UserPassesTestMixin,UpdateView):
    model = Event
    fields = ['name']

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.orgenizer:
            return True
        return False

@login_required
def event_current_song(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    current_song=EventSongs.objects.get(id=event.current_song)
    context = {'event': event,"song" :current_song}
    return render(request, 'event/current_song.html', context)



@login_required
def event_current_song_chords(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    current_song=EventSongs.objects.get(id=event.current_song)
    context = {'event': event,"song" :current_song}
    return render(request, 'event/current_song_chords.html', context)

