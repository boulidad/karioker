# Generated by Django 2.1 on 2020-07-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200709_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_images/default2.jpg', upload_to='profile_pics'),
        ),
    ]
