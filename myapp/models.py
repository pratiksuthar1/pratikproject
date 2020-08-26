from django.db import models

class Contact(models.Model):
	
	name=models.CharField(max_length=100)
	mobile=models.CharField(max_length=10)
	email=models.CharField(max_length=100)
	remarks=models.TextField()

	def __str__(self):
		return self.name

class User(models.Model):

	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	mobile=models.CharField(max_length=10)
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	confirm_password=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="inactive")
	usertype=models.CharField(max_length=100,default="user")
	profile_picture=models.ImageField(upload_to='images/')

	def __str__(self):
		return self.first_name
class Movie(models.Model):
	CHOICES = (
		("romentic",'romentic'),
		("thriller",'thriller'),
		("horror",'horror'),
		("scientific",'scientific'),
	)
	movie_category=models.CharField(max_length=100,choices=CHOICES,default="")
	movie_name=models.CharField(max_length=100)
	language=models.CharField(max_length=100)
	year_of_release=models.CharField(max_length=100)
	director=models.CharField(max_length=100)
	hero=models.CharField(max_length=100)
	heroine=models.CharField(max_length=100)
	movie_image=models.ImageField(upload_to='images/')
	seller_email=models.CharField(max_length=100)


	def __str__(self):
		return self.movie_name
