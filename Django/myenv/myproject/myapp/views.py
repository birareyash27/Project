from urllib import request
from django.shortcuts import render,redirect
from myapp.models import User
from myapp.models import Tour
import random  
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = "User already exists!!"
            return render(request, 'signup.html', {'msg': msg})
        
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    mobile=request.POST['mobile'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype']
                )
                msg = "User created successfully!!"
                return render(request, 'signup.html', {'msg': msg})
    
    return render(request, 'signup.html')  

def login(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)

        email = request.POST.get('email')
        password = request.POST.get('password')

        print("Email:", email)
        print("Password:", password)

        try:
            user = User.objects.get(email=email)
            print("User Found:", user)

            if user.password == password:
                print("Password matched")

                request.session['email'] = user.email

                # Safe profile handling
                if user.profile:
                    request.session['profile'] = user.profile.url

                if user.usertype=="customer":
                    return redirect('index')
                else:
                    return redirect('aindex')    

            else:
                print("Wrong password")
                msg = "Password Does not match!!"
                return render(request, 'login.html', {'msg': msg})

        except Exception as e:
            print("ERROR:", e)
            msg = "Email does not exist!!"
            return render(request, 'login.html', {'msg': msg})

    return render(request, 'login.html')           
def logout(request):
    del request.session['email']
    del request.session['profile']
    return redirect('login')   

def cpass(request):
    if request.method == "POST":
       user = User.objects.get(email=request.session['email'])
       try:
           
            if user.password == request.POST['opassword']:
                if request.POST['password'] == request.POST['cnpassword']:
                   user.password = request.POST['password']
                   user.save()
                   msg = "Password changed successfully!!"
                   return redirect('logout')
                else:
                   msg = "New password and confirm new password do not match!!"
                   return render(request,'cpass.html',{'msg':msg}) 
            else:
                   msg = "Old password is incorrect!!"
                   return render(request,'cpass.html',{'msg':msg})
       except:
            pass
       
    else:
        return render(request,'cpass.html')

def fpass(request):
    if request.method=="POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            subject = 'OTP FOR forgot - password'
            otp = random.randint(1001,9999)
            message = f"Hi {user.name} your otp is : {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject,message,email_from,recipient_list)
            request.session['email']=user.email
            request.session['otp']=otp
            return render(request,'otp.html')
        except:
            msg = "Email Does not exist!!"
            return render(request,'fpass.html',{'msg':msg})

    else:
        return render(request,'fpass.html')

def otp(request):
    if request.method=="POST":
        otp=int(request.session['otp'])
        uotp = request.POST['uotp']
        if otp==uotp:
            del request.session['otp']
            return redirect('newpass')
        else:
            msg = "Invalid OTP!!" 
            return render(request,'otp.html',{'msg':msg})   
    else:            
        return render(request,'otp.html')         

def profile(request):
    user = User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.name = request.POST['name']
        user.mobile = request.POST['mobile']
        try:
            user.profile = request.FILES['profile']
            user.save()
            request.session['profile']=user.profile.url
        except:
            pass
        user.save()
        return redirect('index')
    else:           
        return render(request,'profile.html',{'user':user})
    
def aindex(request):

    return render(request,'aindex.html')

def acpass(request):

    return render(request,'acpass.html')

def addtour(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.get(email=email)

    if request.method == "POST":
        try:
            tcategory = request.POST.get('tcategory')
            tname = request.POST.get('tname')
            tprice = request.POST.get('tprice')
            tlocation = request.POST.get('tlocation')
            days = request.POST.get('days')
            desc = request.POST.get('desc')
            timage = request.FILES.get('timage')

            # 🔥 VALIDATION (this prevents all NULL errors)
            if not all([tcategory, tname, tprice, tlocation, days, desc]):
                return render(request, 'addtour.html', {
                    'msg': 'All fields are required!'
                })

            Tour.objects.create(
                user=user,
                tcategory=tcategory,
                tname=tname,
                tprice=tprice,
                tlocation=tlocation,
                days=days,
                desc=desc,
                timage=timage
            )

            return render(request, 'addtour.html', {
                'msg': 'Tour Added Successfully'
            })

        except Exception as e:
            print("ERROR:", e)
            return render(request, 'addtour.html', {'msg': str(e)})

    return render(request, 'addtour.html')

def viewtour(request):
        
        user = User.objects.get(email=request.session['email'])
        tour = Tour.objects.filter(user=user)

        return render(request, 'viewtour.html', {'tour': tour})

def destination(request):
    return render(request, 'destination.html')

def edit(request, pk):
    user = User.objects.get(email=request.session['email'])
    tour = Tour.objects.get(pk=pk)
    if request.method == "POST":
        tour.tcategory = request.POST.get('tcategory')
        tour.tname = request.POST.get('tname')
        tour.tprice = request.POST.get('tprice')
        tour.tlocation = request.POST.get('tlocation')
        tour.days = request.POST.get('tdays')
        tour.desc = request.POST.get('desc')

        try:
            tour.timage = request.FILES.get('timage')
        except:
            pass

        tour.save()
        return redirect('viewtour')
    return render(request, 'edit.html',{'tour': tour})

def delete(request, pk):
    user= User.objects.get(email=request.session['email'])
    tour = Tour.objects.get(pk=pk)
    tour.delete()
    return redirect('viewtour')


           
              
    
              