# Generated by Django 2.2 on 2020-07-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_movie_seller_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='null', upload_to='images/'),
            preserve_default=False,
        ),
    ]
