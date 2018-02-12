from django.shortcuts import render

from github.models import User
from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def home(requset):
    return render(requset, "github/home.html")

def registration(request):
    return render(request, "github/registration.html")

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

    #send email
    current_site = get_current_site(request)

    mail_subject = 'Activate your BooHub account'
    domain = current_site.domain
    message = ("Hello " + user.firstname + ","
         "\n\n"
         "Thanks for signing up with BooHub!" 
         " You must follow this link to activate your account:"
         "\n\n" + domain + "/github/activate_user/" + user.username +
         "\n\n"
         "Have fun! :)"
         "\n\n"
         "The BooHub Team"
         )
    to_email = user.email

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    return render(request, "github/activate.html", {'user':user})

def activate_user(request,username):
    user = User.objects.get(username=username)
    user.isActive = True
    user.save()
    return render(request, "github/login.html",{'user':user})

def login(requset):
    return render(requset, "github/login.html")
