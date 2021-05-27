from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import joblib
# Create your views here.
@login_required(login_url='loginpage')
def index(request):
	return render(request,("price/index.html"))

def register(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		
		form=CreateUserForm()

		if request.method=="POST":
			form=CreateUserForm(request.POST)
			if form.is_valid():
				form.save()		
				user=form.cleaned_data.get("username")
				messages.success(request,"Account created successfully for " +user)
				return redirect("loginpage")	
		return render(request,("price/register.html"),{"form":form})

def loginpage(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		form=CreateUserForm()
		if request.method=="POST":
			username=request.POST.get("username")
			password=request.POST.get("password")
			user=authenticate(request,username=username,password=password)

			if user is not None:
				login(request,user)
				return redirect("index")
			else:
				messages.info(request,"USERNAME or PASSWORD is incorrect")	
		return render(request,("price/login.html"),{"form":form})

def logoutuser(request):
	logout(request)
	return redirect("loginpage") 	

@login_required(login_url='loginpage')
def result(request):
	#cls=joblib.load("final.sav")
	features=[]
	features.append(request.GET["ppi"])
	features.append(request.GET["mAh"])
	features.append(request.GET["video"])
	features.append(request.GET["os"])
	features.append(request.GET["ram"])
	features.append(request.GET["memory"])

	ans=predict(features)

	return render(request,"price/result.html",{"ans":ans})




























def predict(features):
	ppi=int(features[0])
	mah=int(features[1])
	video=int(features[2])
	os=int(features[3])
	ram=int(features[4])
	memory=int(features[5])

	if ram== 1:
		p=ram1(memory,video,ppi,mah,os)
	elif ram== 2:
		p=ram2(memory,video,ppi,mah,os) 	
	elif ram== 3:
		p=ram3(memory,video,ppi,mah,os) 
	elif ram== 4:
		p=ram4(memory,video,ppi,mah,os) 
	elif ram== 6 :
		p=ram6(memory,video,ppi,mah,os)
	elif ram== 8:
		p=ram8(memory,video,ppi,mah,os)
	else:
		p=5
	return p				

def ram1(memory,video,ppi,mah,os):
	if (ppi>480 and ppi<=720) or (memory>16 and memory<=64):
		return 1
	elif ppi>720 or memory>64 or video>720:
		return 2	
	else:
		
		if   mah>2000  or os >8:
			return 1
		else:
			return 0
	

def ram2(memory,video,ppi,mah,os):
	if (ppi>480 and ppi<=720) or memory>64:
		return 2
	elif ppi>720 or video>1080:
		return 3	
	else:
		
		if  mah>2000 or memory>=32 or os >8:
			return 1
		else:
			return 0
	
def ram3(memory,video,ppi,mah,os):
	if (ppi>480 and ppi<=720) or memory>128 or os>=9:
		return 2
	elif ppi>720 or video >1080:
		return 3	
	else:
		
		if  mah<=5000 or memory<=64 or os<=8:
			return 1
		else:
			return 0
def ram4(memory,video,ppi,mah,os):
	if (ppi>480 and ppi<=1080) or memory>128 or os>=10:
		return 2
	elif ppi>1080 or video >1080 :
		return 3	
	else:
		
		if   mah<=5000 or memory<=64 or os<=9:
			return 2
		else:
			return 1


def ram6(memory,video,ppi,mah,os):
	if (ppi<=1080) or memory>128 or os>10 or video>=4000:
		return 4
	elif ppi<=720 or video>1080 or memory>=64 :
		return 3	
	else:
		
		if memory<=64 or os<=9:
			return 2
		else:
			return 1

def ram8(memory,video,ppi,mah,os):	
	if (ppi<=4000) or memory>128 or os>10 or video>=4000:
		return 5
	elif ppi<=1080 or video>=1080 or memory>=128 :
		return 4	
	else:
		
		if memory<=64 or os<=9:
			return 3
		else:
			return 2
