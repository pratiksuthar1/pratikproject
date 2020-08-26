from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
 	path('contact/',views.contact,name='contact'),
 	path('signup/',views.signup,name='signup'),
 	path('verify_otp/',views.verify_otp,name='verify_otp'),
 	path('login/',views.login,name='login'),
 	path('enter_email/',views.enter_email,name='enter_email'),
 	path('get_otp/',views.get_otp,name='get_otp'),
 	path('forget_password/',views.forget_password,name='forget_password'),
 	path('change_password/',views.change_password,name='change_password'),
 	path('logout/',views.logout,name='logout'),
 	path('add_movie/',views.add_movie,name='add_movie'),
  	path('view_movie/',views.view_movie,name='view_movie'),
  	path('seller_index/',views.seller_index,name='seller_index'),
  	path('movie_detail/<int:pk>/',views.movie_detail,name='movie_detail'),


 ]
