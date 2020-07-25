from django.shortcuts import render,redirect
from django.contrib import messages
from .utils import *
from karioker.models import *

def scrape_tab4u(request):
    if request.method=='POST':
        print(request.POST['fname'])
        song_data = get_data_for_one_url(request.POST['fname'])
        song=get_create_song(song_data)
        song_name=song_data['title']
        if song['status']=='new_song_created':
        	messages.success(request,f'{song_name} was scraped and added to our database, thanks!')
        elif song['status']=='song_already_exists':
        	messages.success(request,f'{song_name} already exists in our database, please check it out here:')
        return redirect(reverse('song-detail', kwargs={'pk': song['song'].id}))
    else:    
        print('no data yet')
    return render(request,'crawler/scrape_tab4u.html')

# Create your views here.
