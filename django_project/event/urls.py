from django.urls import path
from . import views
from .views import *
#EventListView,EventDetailView,EventCreateView,EventUpdateView,EventDeleteView,event_with_details,kafka_connect,KafkaConnect

urlpatterns = [
    path('', EventListView.as_view(),  name='events-home'),
    #path('nondetailed/<int:pk>/', EventDetailView.as_view(),  name='not-event-detail'),
    path('<int:pk>/update/', EventUpdateView.as_view(),  name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(),  name='event-delete'),
    path('new/', EventCreateView.as_view(),  name='event-create'),
    path('<int:pk>/', event_with_details, name='event-detail'),
    #path('kafka-connect/', kafka_connect,  name='kafka-connect'),
    #path('kafkaconnect/', KafkaConnect.as_view(),  name='kafka-connect'),
    path('<int:event_id>/add_guest/', AddEventGuest.as_view(),  name='event-add-guest'),
    path('<int:event_id>/join/<str:token>', join_event,  name='event-join'),
    path('<int:event_id>/add_song/<int:song_id>/', event_add_song,  name='event-add-song'),
    path('event_song_delete/<int:event_song_id>/', event_delete_song,  name='event-delete-song'),

]


