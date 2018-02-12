from django.shortcuts import render


from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from github.models import User, Organization, Repository



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


def organization(request):
    organization = Organization()
    return render(request, 'github/organization.html', {'organization' : organization})

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

    # set name in session
    request.session['name'] = name

    return render(request, 'github/organizationDetails.html', {'organization':organization})

def saveOrganizationDetails(request):
    purpose = request.POST['purpose']
    howLong = request.POST['howLong']
    howMuchPeople = request.POST['howMuchPeople']

    # get name from session
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



def repository(request):
    repository = Repository()
    return render(request, 'github/repository.html', {'repository':repository})

def saveRepository(request):
    name = request.POST['name']
    description = request.POST['description']
    type = request.POST['type']
    repository = Repository()
    repository.name = name
    repository.description = description
    repository.type = type
    repository.save()
    # put name in session
    request.session['nameRepository'] = repository.name
    return render(request, 'github/repositoryMembers.html', {'repository': repository})

def saveRepositoryMembers(request):
    memberName = request.POST['memberRepository']
    # get name from session
    nameRepository= request.session['nameRepository']
    repository = Repository()
    repositories = Repository.objects.all()
    users = User.objects.all()
    usernameList = []

    # find organization
    for r in repositories:
        if r.name == nameRepository:
            repository = r
    # list with all usernames
    for u in users:
        usernameList.append(u.username)
    # check username
    if memberName not in usernameList:
        return render(request, 'github/repositoryMembers.html',
                      {'message': 'Username does not exist.', 'repository': repository})
    else:
        for m in users:
            if m.username == memberName:
                repository.members.add(m)
                repository.save()
                membersRepository = repository.members.all
                return render(request, 'github/repositoryDetails.html',
                              {'repository': repository, 'membersRepository': membersRepository})

    return render(request, 'github/repositoryDetails.html', {'repository':repository})

def repositoriesShow(request):
    repositories = Repository.objects.all()
    return render(request, 'github/repositoriesShow.html', {'repositories':repositories})
