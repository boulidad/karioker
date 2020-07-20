from django.urls import path
from . import views
from .views import SongsListView,SongsDetailView,SongsChordsView,SongCreateView,SongUpdateView,SongDeleteView,PerformerSongsListView

urlpatterns = [
    path('', views.home,  name='karioker-home'),
    path('about/', views.about,  name='karioker-about'),
    path('songs/', SongsListView.as_view(),  name='karioker-songs'),
    path('song/<int:pk>/', SongsDetailView.as_view(),  name='song-detail'),
    path('performer_songs/<str:performer_name>/', PerformerSongsListView.as_view(),  name='performer-songs'),
    path('song-chords/<int:pk>/', SongsChordsView.as_view(),  name='song-chords'),
    path('song/<int:pk>/update/', SongUpdateView.as_view(),  name='song-update'),
    path('song/<int:pk>/delete/', SongDeleteView.as_view(),  name='song-delete'),
    path('song/new/', SongCreateView.as_view(),  name='song-create'),
]
