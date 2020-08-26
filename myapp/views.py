from django.shortcuts import render
from .models import Contact,User,Movie
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.serializers.json import DjangoJSONEncoder
import json

def index(request):
	return render(request,'myapp/index.html')

def contact(request):
	if request.method=="POST":
		name=request.POST['name']
		mobile=request.POST['mobile']
		email=request.POST['email']
		remarks=request.POST['remarks']
		Contact.objects.create(name=name,mobile=mobile,email=email,remarks=remarks)
		msg="contact saved successfully"
		return render(request,'myapp/contact.html',{'msg':msg})
	else:
		return render(request,'myapp/contact.html')


def signup(request):
	if request.method=="POST":
		user=User()
		user.usertype=request.POST['usertype']
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.password=request.POST['password']
		user.cpassword=request.POST['cpassword']
		user.profile_picture=request.FILES['profile_picture']
		a=User.objects.filter(email=user.email)
		if a:
			msg="email already exist Please use another Email ID"
			return render(request,'myapp/signup.html',{'msg':msg})
		elif user.password!=user.cpassword:
			msg="password and confirm Password Does not Match"
			return render(request,'myapp/signup.html',{'msg':msg,'user':user})
		else:
			rec=[user.email,]
			subject="OTP for Registration"
			otp=random.randint(1000,9999)
			message="your OTP for Registration is "+str(otp)
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			User.objects.create(first_name=user.fname,last_name=user.lname,mobile=user.mobile,email=user.email,password=user.password,confirm_password=user.cpassword,usertype=user.usertype,profile_picture=user.profile_picture)
			# return render(request,'myapp/verify_otp.html',{'otp':otp,'email':email})
			# msg="Signup successfully"
			msg="enter OTP"
			return render(request,'myapp/verify_otp.html',{'msg':msg,'otp':otp,'email':user.email})
	else:
		return render(request,'myapp/signup.html')

def verify_otp(request):
	if request.method=="POST":
		otp=request.POST['otp']
		u_otp=request.POST['u_otp']
		email=request.POST['email']
		if otp==u_otp:
			user=User.objects.get(email=email)
			if user.status=="active":
				return render(request,'myapp/new_password.html',{'email':email})
			else:
				user.status="active"
				user.save()
				msg="Your Account is now Generated Please Login"
				return render(request,'myapp/login.html',{'msg':msg})
		else:
			msg="OTP or Email are not Correct Please Signup again"
			return render(request,'myapp/signup.html',{'msg':msg})
	else:
		return render(request,'myapp/signup.html')

def login(request):
	if request.method=="POST":
		email=request.POST['email']
		password=request.POST['password']
		try:
			user=User.objects.get(email=email,password=password)
			if user.status=="active"and user.usertype=="user":
				request.session['fname']=user.first_name
				request.session['email']=user.email
				return render(request,'myapp/index.html')
			elif user.status=="active" and user.usertype=="seller":
				request.session['fname']=user.first_name
				request.session['email']=user.email
				return render(request,'myapp/seller_index.html')
			else:
				msg="you still not active your account please activate again"
				return render(request,'myapp/enter_email.html',{'msg':msg})
		except:
			msg="Email or Password does not Exist"
			return render(request,'myapp/login.html',{'msg':msg})
	else:
		return render(request,'myapp/login.html')
# Create your views here.
def forget_password(request):
	email=request.POST['email']
	password=request.POST['password']
	cpassword=request.POST['cpassword']
	if password==cpassword:
		user=User.objects.get(email=email)
		user.password=password
		user.confirm_password=cpassword
		user.save()
		msg="password updates successfully"
		return render(request,'myapp/login.html',{'msg':msg})
	else:
		msg="password and confirm password does not match."
		return render(request,'myapp/new_password.html')

def enter_email(request):
	return render(request,'myapp/enter_email.html')

def get_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		user=User.objects.get(email=email)
		if user:
			rec=[email,]
			subject="OTP for Password Reset"
			otp=random.randint(1000,9999)
			message="your OTP for Password reset is "+str(otp)
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			return render(request,'myapp/verify_otp.html',{'otp':otp,'email':email})
		else:
			return render(request,'myapp/login.html')
	else:
		return render(request,'myapp/enter_email.html')

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		print(user)
		opassword=request.POST['opassword']
		npassword=request.POST['npassword']
		cnpassword=request.POST['cnpassword']
		if user.password!=opassword:
			msg="Old Password Does'nt Match"
			return render(request,'myapp/change_password.html',{'msg':msg})
		elif npassword!=cnpassword:
			msg="New Password and confirm New Password Does'nt Match"
			return render(request,'myapp/change_password.html',{'msg':msg})
		else:
			user.password=npassword
			user.confirm_password=cnpassword
			user.save()
			try:
				del request.session['fname']
				del request.session['email']
				msg="your password saved successfully"
				return render(request,'myapp/login.html',{'msg':msg})
			except:
				pass
	return render(request,'myapp/change_password.html')

def logout(request):
	try:
		del request.session['fname']
		del request.session['email']
		return render(request,'myapp/login.html')
	except:
		return render(request,'myapp/login.html')
	
def add_movie(request):
	if request.method=="POST":
		movie_category=request.POST['movie_category']
		movie_name=request.POST['movie_name']
		language=request.POST['language']
		year=request.POST['year']
		director=request.POST['director']
		hero=request.POST['hero']
		heroine=request.POST['heroine']
		movie_image=request.FILES['movie_image']
		seller_email=request.session['email']

		Movie.objects.create(movie_category=movie_category,movie_name=movie_name,language=language,year_of_release=year,director=director,hero=hero,heroine=heroine,movie_image=movie_image,seller_email=seller_email)
		msg="Movie added successfully"
		return render(request,'myapp/add_movie.html',{'msg':msg})
	else:
		return render(request,'myapp/add_movie.html')

def view_movie(request):
	movies=Movie.objects.filter(seller_email=request.session['email'])
	return render(request,'myapp/view_movie.html',{'movies':movies})
def seller_index(request):
	return render(request,'myapp/seller_index.html')

def movie_detail(request,pk):
	movies=Movie.objects.get(pk=pk)
	return render(request,'myapp/movie_detail.html',{'movies':movies})


