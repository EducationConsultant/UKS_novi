from django.shortcuts import render

from github.models import User, Organization


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








