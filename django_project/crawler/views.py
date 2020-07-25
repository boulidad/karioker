from django.shortcuts import render
from .utils import *

def scrape_tab4u(request):
    if request.method=='POST':
        print(request.POST)
        #song_data = get_data_for_one_url(request.POST)
        #print(song_data)
    else:    
        print('no data yet')
    return render(request,'crawler/scrape_tab4u.html')

# Create your views here.
