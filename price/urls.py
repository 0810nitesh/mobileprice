from django.urls import path
from . import views

urlpatterns=[
		path("",views.index,name="index"),
		path("result",views.result,name="result"),
		path('register/',views.register,name="register"),
		path('loginpage/',views.loginpage,name="loginpage"),
		path('logoutuser/',views.logoutuser,name="logoutuser")		
]