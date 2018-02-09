from django.shortcuts import render

from github.models import User


def home(requset):
    return render(requset, 'github/home.html')

def registration(request):
    return render(request, 'github/registration.html')

def saveUser(request):
    username = request.POST['username']

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    password = request.POST['password']
    email = request.POST['email']

    user = User()
    user.firstname = firstname
    user.lastname = lastname
    user.username = username
    user.password = password
    user.email = email

    #unique username
    users = User.objects.all()
    for u in users:
        if u.username == username:
            return render(request, 'github/registration.html',{'message':'Username must be unique.','user':user})

    user.save()

    #print all users
    #users = User.objects.all()
    #for u in users:
        #print(u.__str__())

    return render(request, 'github/login.html', {'user':user})

def login(requset):
    return render(requset, 'github/login.html')