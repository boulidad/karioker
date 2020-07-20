from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from event.models import Event
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    context = {
        'songs' : Songs.objects.all()
    }
    return render(request,'karioker/home.html',context)

def about(request):
    return render(request,'karioker/about.html', { "title" : "About" } )

def songs(request):
    context = {
        'songs' : Songs.objects.all()
    }
    return render(request,'karioker/songs.html',context)

class SongsListView(ListView):
    #print (self.kwargs)
    #. price_lte = request.GET['price_lte']
    model = Songs
    context_object_name = 'songs'
    paginate_by=500
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.request.GET.get("event_id", None)
        print(f'the event is {event_id}')
        if event_id: 
            try:
                context['event'] = Event.objects.get(id=event_id)
                context['in_event'] = True
            except ObjectDoesNotExist:
                context['in_event'] = False
            except ValueError:
                context['in_event'] = False
        else:
            context['in_event'] = False
        return context


class PerformerSongsListView(ListView):
    template_name='karioker/peformer_songs.html'
    model = Songs
    context_object_name = 'songs'
    paginate_by=200
    def get_queryset(self):
        performer_id = get_object_or_404(Performers, name=self.kwargs.get('performer_name'))
        return Songs.objects.filter(performer=performer_id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.request.GET.get("event_id", None)
        print(f'the event is {event_id}')
        if event_id: 
            try:
                context['event'] = Event.objects.get(id=event_id)
                context['in_event'] = True
            except ObjectDoesNotExist:
                context['in_event'] = False
            except ValueError:
                context['in_event'] = False
        else:
            context['in_event'] = False
        return context



class SongsDetailView(DetailView):
    model = Songs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.request.GET.get("event_id", None)
        if event_id: # and isinstance(event_id, int):
            try:
                context['event'] = Event.objects.get(id=event_id)
                context['in_event'] = True
            except ObjectDoesNotExist:
                context['in_event'] = False
            except ValueError:
                context['in_event'] = False
        else:
            context['in_event'] = False
        return context

#        print(**kwargs)
#        return self.request

        #self.object_list = self.get_queryset()
        #self.object_list = self.object_list.filter(lab__acronym=kwargs['lab'])

class SongsChordsView(DetailView):
    template_name='karioker/songs_chords.html'
    model = Songs

class SongCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Songs
    fields = ['name','performer','songwriter','composer','lyrics','chords']
    def test_func(self):
        return self.request.user.is_staff

class SongDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Songs
    success_url = '/songs/'
    def test_func(self):
        return self.request.user.is_staff

class SongUpdateView(UserPassesTestMixin,UpdateView):
    model = Songs
    fields = ['name','performer','songwriter','composer','lyrics','chords']

    def test_func(self):
        return self.request.user.is_staff
