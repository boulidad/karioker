from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Songs)
admin.site.register(Composers)
admin.site.register(Performers)
admin.site.register(SongWriters)
