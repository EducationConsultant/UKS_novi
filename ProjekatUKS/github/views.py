from django.shortcuts import render


from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site

from github.models import User, Organization


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
    return render(request, "github/login.html")

def login(requset):
    return render(requset, "github/login.html")

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
        if user.password == password:
            user.loggedin = True
            user.save()

            request.session['id_user'] = id(user)
            request.session['uname_user'] = user.username


            return render(request, "github/afterUserLogin.html")
        else:
            return render(request, "github/login.html",{'message':'Incorrect password.','uname':username})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'User does not exist.'})

def logout(request):
    request.session['uname_user'] = None
    return render(request, "github/login.html")

def about_user(request):
    username = request.session['uname_user']
    user = User.objects.get(username=username)

    return render(request, "github/about_user.html",{'user':user})

def change_username(request):
    return render(request, "github/change_username.html")

def change_password(request):
    return render(request, "github/change_password.html")

def delete_account(request):
    return render(request, "github/delete_account.html")


def organization(request):
    return render(request, 'github/organization.html')

def saveOrganization(request):
    name = request.POST['name']
    email = request.POST['email']
    organizations = Organization.objects.all()
    organization = Organization()
    organization.email = email

    # check if name exists
    for o in organizations:
        if o.name == name:
            return render(request, 'github/organization.html',
                          {'organization': organization, 'message': 'That name already exists!'})
    organization.name = name
    organization.save()
    request.session['name'] = name
    return render(request, 'github/organizationDetails.html', {'organization':organization})

def saveOrganizationDetails(request):
    purpose = request.POST['purpose']
    howLong = request.POST['howLong']
    howMuchPeople = request.POST['howMuchPeople']
    name = request.session['name']
    organization = Organization()
    organizations = Organization.objects.all()
    for o in organizations:
        if o.name == name:
            o.purpose = purpose
            o.howLong = howLong
            o.howMuchPeople = howMuchPeople
            o.save()
            organization = o
    return render(request, 'github/organizationMembers.html', {'organization': organization})

def saveOrganizationMembers(request):
    memberName=request.POST['member']
    nameOrganization = request.session['name']
    organization = Organization()
    organizations = Organization.objects.all()
    users = User.objects.all()
    usernameList = []
    # find organization
    for o in organizations:
        if o.name == nameOrganization:
            organization = o
    # list with all usernames
    for u in users:
        usernameList.append(u.username)
    # check username
    if memberName not in usernameList:
        return render(request, 'github/organizationMembers.html',
                      {'message': 'Username does not exist.', 'organization': organization})
    else:
        for m in users:
            if m.username == memberName:
                organization.members.add(m)
                organization.save()
                membersOrganization = organization.members.all
                return render(request, 'github/organizationInfo.html',
                              {'organization': organization, 'membersOrganization': membersOrganization})






