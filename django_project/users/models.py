from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import random


class Profile(models.Model):
	#random_default_picture='default_images/default'+str(random.randint(1, 8))+'.jpg'
	random_default_picture='default_images/default3.jpg'
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default=random_default_picture, upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

#	def save(self):
#		super().save()
#
#		img=Image.open(self.image.path)
#		if img.height>300 or img.width >300:
#			output_size = (300,300)
#			img.thumbnail(output_size)
#			img.save(self.image.path)

