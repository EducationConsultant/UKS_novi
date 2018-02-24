from django.shortcuts import render
import os

from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from github.models import User, Organization, Repository, Issue, Comment, Milestone, Label, History, Wiki

# switch from some page to home.html
def switch_home(requset):
    return render(requset, "github/home.html")


# switch from some page to registration.html
def switch_registration(request):
    return render(request, "github/registration.html")


# registrate new user
# unique username and email
# switch to activate.html
def save_user(request):
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
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/registration.html', {'message': 'Username must be unique.', 'user': user})
    except User.DoesNotExist:
        user.username=username

    #unique email
    try:
        user = User.objects.get(email=email)
        return render(request, 'github/registration.html', {'messageEmail': 'Email must be unique.', 'user': user})
    except User.DoesNotExist:
        user.save()

    #send email
    current_site = get_current_site(request)

    mail_subject = 'Activate your BooHub account'
    domain = current_site.domain
    message = ("Hello " + user.firstname + ","
         "\n\n"
         "Thanks for signing up with BooHub!" 
         " You must follow this link to activate your account:"
         "\n\n" + domain + "/boohub/activate_user/" + user.username +
         "\n\n"
         "Have fun! :)"
         "\n\n"
         "The BooHub Team"
         )

    email = EmailMessage(mail_subject, message, from_email = None, to = None, bcc = [user.email,],
    connection = None, attachments = None, headers = None, cc = None)

    email.send()

    return render(request, "github/activate.html", {'user':user})


# from email link to login.html
def activate_user(request,username):
    try:
        user = User.objects.get(username=username)
        user.isActive = True
        user.save()
        return render(request, "github/login.html")
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'User does not exist.'})

# from some page to login.html
def switch_login(requset):
    return render(requset, "github/login.html")


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
        if user.isActive:
            if user.password == password:
                user.loggedin = True
                user.save()

                request.session['uname_user'] = user.username
                request.session['loggedin'] = 'True'

                owner_repositories = Repository.objects.filter(owner=user.pk)
                member_repositories = Repository.objects.filter(members=user.pk)

                repositories = (owner_repositories | member_repositories).distinct()

                return render(request, "github/home.html",{'repositories':repositories})
            else:
                return render(request, "github/login.html",{'message':'Incorrect password.','uname':username})
        else:
            return render(request, "github/login.html", {'message': 'Account is not activated.'})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'User does not exist.'})


# from some page to forgot_password.html
def switch_forgot_password(request):
    return render(request, "github/forgot_password.html")


def send_email_reset_password(request):
    email = request.POST.get('email')

    try:
        user = User.objects.get(email=email)

        # send email
        current_site = get_current_site(request)

        mail_subject = 'Please reset your password'
        domain = current_site.domain
        message = ("Hello " + user.firstname + ","
                    "\n\n"
                    "We heard that you lost your BooHub password. Sorry about that!"
                    " But don’t worry! You can use the following link to reset your password:"
                    "\n\n" + domain + "/boohub/password_reset/" + user.username +
                   "\n\n"
                   "The BooHub Team"
                   )

        email = EmailMessage(mail_subject, message, from_email=None, to=None, bcc=[user.email, ],
                             connection=None, attachments=None, headers=None, cc=None)
        email.send()

        return render(request, "github/password_reset.html", {'user':user})
    except User.DoesNotExist:
        return render(request, "github/forgot_password.html", {'message': 'User does not exist.'})


def switch_forgot_password_reset(request,username):
    request.session['uname_user'] = username
    try:
        user = User.objects.get(username=username)
        return render(request, "github/forgot_password_reset.html", {'username': username})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def reset_password(request):
    newpassword = request.POST.get('newpassword')
    confirmnewpassword = request.POST.get('confirmnewpassword')

    username=request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        if newpassword == confirmnewpassword:
            user.password = newpassword
            user.save()

            return render(request, "github/login.html")
        else:
            return render(request, "github/forgot_password_reset.html",
                          {'message': 'Password does not match the confirmation.'})
    except User.DoesNotExist:
        return render(request, "github/forgot_password_reset.html", {'message': 'User does not exist.'})


def logout(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        user.loggedin = False
        user.save()

        request.session['uname_user'] = None
        request.session['loggedin'] = None
        request.session['repository_id'] = None
        request.session['nameOrganization'] = None
        return render(request, "github/login.html")
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

def about_user(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, "github/about_user.html",{'user':user})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_change_username(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, "github/change_username.html")
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def change_username(request):
    newusername = request.POST.get('newusername')

    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        user.username = newusername
        user.save()
        request.session['uname_user'] = user.username

        return render(request, "github/change_username.html", {'messageNew': 'Username successfully changed.'})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_change_password(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, "github/change_password.html")
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def change_password(request):
    oldpassword = request.POST.get('oldpassword')
    newpassword = request.POST.get('newpassword')
    confirmnewpassword = request.POST.get('confirmnewpassword')

    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        if user.password == oldpassword:
            if newpassword == confirmnewpassword:
                user.password = newpassword
                user.save()

                return render(request, "github/change_password.html", {'messageNew': 'Password successfully changed.'})
            else:
                return render(request, "github/change_password.html", {'messageConfirmationPass': 'Password does not match the confirmation.'})
        else:
            return render(request, "github/change_password.html", {'messageOldPass': 'Old password is not valid.'})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_delete_account(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, "github/delete_account.html")
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def delete_account(request):
    usernameI = request.POST.get('username')
    passwordI = request.POST.get('password')

    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        if user.username == usernameI:
            if user.password == passwordI:
                request.session['uname_user'] = None
                request.session['loggedin'] = None
                user.delete()

                return render(request, "github/home.html")
            else:
                return render(request, "github/delete_account.html", {'messagePassword': 'Password is not valid.'})
        else:
            return render(request, "github/delete_account.html", {'messageUsername': 'Username is not valid.'})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

def switch_delete_organization(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/delete_organization.html', {'name': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_delete_milestone(request, id):
    milestone = Milestone.objects.get(pk=id)
    nameRepository = milestone.repository.name
    milestonesOfRepository = getMilestonesOfRepository(nameRepository)
    return render(request, 'github/delete_milestone.html', {'milestone':milestone,
                                                            'milestonesOfRepository': milestonesOfRepository,
                                                            'nameRepository':nameRepository})

def switch_delete_repository(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/delete_repository.html', {'name': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_edit_repository(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/edit_repository.html', {'name': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_edit_organization(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/edit_organization.html', {'name': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def edit_organization(request, name):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)

        nameEdit = request.POST.get('nameEdit')

        organization = Organization.objects.get(name=name)
        organization.name = nameEdit
        organization.save()

        owner_organizations = Organization.objects.filter(owner=user.pk)
        member_organizatios = Organization.objects.filter(members=user.pk)

        organizations = (owner_organizations | member_organizatios).distinct()

        return render(request, 'github/organizationsShow.html', {'username': username,
                                                                 'organizationsOfUser': organizations})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def delete_organization(request, name):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)
        owner_organizations = Organization.objects.filter(owner=user.pk)
        member_organizatios = Organization.objects.filter(members=user.pk)

        organizations = (owner_organizations | member_organizatios).distinct()
        try:
            organization = Organization.objects.get(name=name)
            nameDelete = request.POST.get('nameDelete')

            if name == nameDelete:
                organization.delete()
                return render(request, 'github/organizationsShow.html',{'username': username,
                                                                     'organizationsOfUser': organizations})
            else:
                return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})

        except Organization.DoesNotExist:
            return render(request, 'github/organizationsShow.html', {'username': username,
                                                                     'organizationsOfUser': organizations})

    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def edit_repository(request, name):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)

        nameEdit = request.POST.get('nameEdit')

        repository = Repository.objects.get(name=name)
        repository.name = nameEdit
        repository.save()

        owner_reoisitories = Repository.objects.filter(owner=user.pk)
        member_repositories = Repository.objects.filter(members=user.pk)

        repositories = (owner_reoisitories | member_repositories).distinct()

        return render(request, 'github/repositoriesShow.html',{'username': username,
                                                                 'repositoriesOfUser': repositories})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def delete_repository(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        owner_reoisitories = Repository.objects.filter(owner=user.pk)
        member_repositories = Repository.objects.filter(members=user.pk)

        repositories = (owner_reoisitories | member_repositories).distinct()
        try:
            repository = Repository.objects.get(name=name)
            nameDelete = request.POST.get('nameDelete')
            if name == nameDelete:
                repository.delete()
                return render(request, 'github/repositoriesShow.html', {'username': username,
                                                                    'repositoriesOfUser': repositories})
            else:
                return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})
        except Repository.DoesNotExist:
            return render(request, 'github/repositoriesShow.html', {'username': username,
                                                                    'repositoriesOfUser': repositories})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def organization(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        organization = Organization()
        return render(request, 'github/organization.html', {'organization': organization})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def saveOrganization(request):
    #owner
    username = request.session['uname_user']
    try:
        owner = User.objects.get(username=username)

        name = request.POST['name']
        email = request.POST['email']
        organizations = Organization.objects.all()
        users = User.objects.all()
        organization = Organization()

        # check fileds empty
        if name == "":
            return render(request, 'github/organization.html',
                          {'organization': organization, 'messageName': ' Field name must be filled!'})
        if email == "":
            return render(request, 'github/organization.html',
                          {'organization': organization, 'messageEmail': ' Field email must be filled!'})

        # check if name exists
        organization.name = name
        organization.email = email
        try:
            org = Organization.objects.get(name=name)
            return render(request, 'github/organization.html',
                          {'organization': organization, 'messageName': 'That name already exists!'})
        except Organization.DoesNotExist:
            organization.name = name

        organization.email = email
        organization.owner = owner
        organization.save()

        # put owner into members of organization
        organization.members.add(owner)
        organization.save()
        organizationMembers = organization.members.all

        # set nameOrganization in session
        request.session['nameOrganization'] = name

        return render(request, 'github/organizationDetails.html', {'organization':organization, 'organizationMembers': organizationMembers})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def saveOrganizationDetails(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        purpose = request.POST['purpose']
        howLong = request.POST['howLong']
        howMuchPeople = request.POST['howMuchPeople']

        # get nameOrganization from session
        nameOrganization = request.session['nameOrganization']

        organization = Organization.objects.get(name=nameOrganization)
        organization.purpose = purpose
        organization.howLong = howLong
        organization.howMuchPeople = howMuchPeople
        organization.save()

        return render(request, 'github/addNewMemberOrganization.html', {'organization': organization})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def saveOrganizationMembers(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        # find organization
        organization = Organization.objects.get(name=name)

        memberName=request.POST['member']

        users = User.objects.all()
        usernameList = []

        # list with all usernames
        for u in users:
            usernameList.append(u.username)

        # check username
        if memberName not in usernameList:
            return render(request, 'github/addNewMemberOrganization.html',
                          {'message': 'Username does not exist.', 'organization': organization})
        else:
            member = User.objects.get(username=memberName)
            organization.members.add(member)
            organization.save()

            owner_repositories = Repository.objects.filter(owner=user.pk)
            member_repositories = Repository.objects.filter(members=user.pk)

            repositories = (owner_repositories | member_repositories).distinct()

            return render(request, 'github/organizationInformations.html',
                                  {'p':organization.name,'organization': organization,'repositories':repositories})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# get all organizations by user ( owner and member)
def organizationsByUser(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        owner_organizations = Organization.objects.filter(owner=user.pk)
        member_organizatios = Organization.objects.filter(members=user.pk)

        organizations = (owner_organizations | member_organizatios).distinct()

        return render(request, 'github/organizationsShow.html', {'username': username,
                                                                 'organizationsOfUser':organizations})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

# new repository
def repository(request,p):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        organization = Organization.objects.get(name=p)
        repository = Repository()
        return render(request, 'github/repository.html',{'organization':organization,'repository':repository,'p':organization.name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# save new repository
def saveRepository(request, p):
    organization = Organization.objects.get(name=p)
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)

        name = request.POST['name']
        description = request.POST['description']
        type = request.POST['type']

        repository = Repository()
        repository.name = name
        repository.description = description
        repository.type = type
        repository.organization = organization
        repository.owner = user


        try:
            org = Repository.objects.get(name=name)
            return render(request, 'github/repository.html',
                          {'repository': repository,'organization':organization, 'p': p, 'messageName': 'That name already exists!'})
        except Repository.DoesNotExist:
            repository.save()

        # put owner into members of repository
        repository.members.add(user)
        repository.save()

        wiki = Wiki()
        wiki.content = ""
        wiki.title = "Wiki of " + str(repository.name)
        wiki.save()
        repository.wiki = wiki
        repository.save()

        request.session['repository_id'] = repository.pk
        repositoryMembers = repository.members.all
        return render(request, 'github/addNewMemberRepository.html',
                  {'repository': repository, 'repositoryMembers': repositoryMembers, 'p': p})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# parametar 'name' is nameRepostiory
def saveRepositoryMembers(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        # find rpeository
        repository = Repository.objects.get(name=name)

        memberName = request.POST['member']

        users = User.objects.all()
        usernameList = []


        # list with all usernames
        for u in users:
            usernameList.append(u.username)
        # check username
        if memberName not in usernameList:
            return render(request, 'github/addNewMemberRepository.html',
                          {'message': 'Username does not exist.', 'repository': repository})
        else:
            member = User.objects.get(username=memberName)
            repository.members.add(member)
            repository.save()

            repositoryMembers = repository.members.all
            return render(request, 'github/repositoryInformations.html',
                                  {'repository': repository, 'repositoryMembers': repositoryMembers})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# shows all organisations
def organizationsShow(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        organizations = Organization.objects.all()
        return render(request, 'github/organizationsShow.html', {'organizations':organizations })
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# informations about one organization
def organizationInfo(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        organization = Organization.objects.get(name=name)

        organizationMembers = organizationMembersShow(organization)
        organizationRepositories = getRepositoriesByOrganization(name)

        return render(request, 'github/organizationInformations.html', {'organization': organization,
                                                                'organizationMembers': organizationMembers,
                                                                'repositories':organizationRepositories})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# returns all members of one organziation
def organizationMembersShow(organization):
    organizationMembers = organization.members.all()
    return organizationMembers

# returns all members of one repository
def repositoryMembersShow(repository):
    repositoryMembers = repository.members.all()
    return repositoryMembers

# new member in organization
def addNewMemberOrganization(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        organization = getOrganizationByName(name)
        return render(request, 'github/addNewMemberOrganization.html', {'organization': organization})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

# new member in repository, name is repositoryName
def addNewMemberRepository(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository = getRepositoryByName(name)
        return render(request, 'github/addNewMemberRepository.html', {'repository': repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# returns organization by name
def getOrganizationByName(nameOrganization):
    organization = Organization()
    organizations = Organization.objects.all()
    for o in organizations:
        if o.name == nameOrganization:
            organization = o
    return organization

# returns repository by name
def getRepositoryByName(nameRepository):
    repository = Repository()
    repositories = Repository.objects.all()
    for r in repositories:
        if r.name == nameRepository:
            repository = r
    return repository


# get repositories of user
def repositoriesShow(request):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)

        owner_repositories = Repository.objects.filter(owner=user.pk)
        member_repositories = Repository.objects.filter(members=user.pk)

        repositories = (owner_repositories | member_repositories).distinct()

        return render(request, 'github/repositoriesShow.html', {'username': username, 'repositoriesOfUser':repositories })
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# returns all repositories of organization
def getRepositoriesByOrganization(nameOrganization):
    repositories = Repository.objects.all()
    organizationRepositories = []
    for r in repositories:
        if r.organization.name == nameOrganization:
            organizationRepositories.append(r)
    return organizationRepositories

# informations about one repository
def repositoryInfo(request, name):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)
        repositories = Repository.objects.all()
        repository = Repository()
        for r in repositories:
            if r.name == name:
                repository = r
        repositoryMembers = repositoryMembersShow(repository)

        repository = Repository.objects.get(name=name)
        request.session['repository_id'] = repository.pk
        request.session['repository_name'] = repository.name

        return render(request, 'github/repositoryInformations.html', {'repository': repository,
                                                                    'repositoryMembers': repositoryMembers})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_issue_show_all(request):
    username = request.session['uname_user']

    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issues = Issue.objects.filter(repository=repository.pk)
        return render(request, "github/issue_show_all.html",{'issues':issues,
                                                             'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_show_all_open(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issues = Issue.objects.filter(closed=False)
        return render(request, "github/issue_show_all.html",{'issues': issues,
                                                             'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_show_all_closed(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issues = Issue.objects.filter(closed=True)
        return render(request, "github/issue_show_all.html",{'issues': issues,
                                                             'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_issue_new(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        milestonesAll = Milestone.objects.all()
        milestones = []   # just opened milestones

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)

        users=[]
        if repository.members.all() is not None:
            for member in repository.members.all():
                users.append(member.username)

        labels = Label.objects.filter(repository=repository.pk)
        return render(request, "github/issue_new.html", {'users':users,'labels':labels,
                                                         'milestones': milestones,
                                                         'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_new(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        title = request.POST.get('title')
        description = request.POST.get('description')
        listAssignees = request.POST.getlist('assignees')
        listLabels = request.POST.getlist('labels')
        milestoneTitle = request.POST.get('milestone')

        milestonesAll = Milestone.objects.all()
        milestones = []  # just opened milestones

        issue = Issue()
        issue.title = title
        issue.description = description
        issue.author = user
        issue.repository = repository

        if milestoneTitle != "":
            milestone = Milestone.objects.get(title=milestoneTitle)
            issue.milestone = milestone
            milestone.countOpenedIssues = milestone.countOpenedIssues + 1
            milestone.save()
        issue.save()

        for ass in listAssignees:
            user = User.objects.get(username=ass)
            issue.assignees.add(user)
        issue.save()

        for lab in listLabels:
            label = Label.objects.get(name=lab)
            issue.labels.add(label)
        issue.save()

        comments = Comment.objects.filter(issue=issue.pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)

        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",{'issue':issue,
                                                             'comments':comments,
                                                             'labels':result_labels,
                                                             'milestones':milestones,
                                                             'history':all_history,
                                                             'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# CREATE ISSUE FROM MILESTONE
# name is nameMilestone
def switch_issue_new_from_milestone(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        users = []
        if repository.members.all() is not None:
            for member in repository.members.all():
                users.append(member.username)
        labels = Label.objects.filter(repository=repository.pk)
        return render(request, "github/issue_new_from_milestone.html", {'users': users, 'labels': labels,
                                                         'milestoneTitle': name,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

# FROM MILESTONE
# name is nameMilestone
def issue_new_from_milestone(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        milestones = []  # just opened milestones
        milestonesAll = Milestone.objects.all()

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)

        title = request.POST.get('title')
        description = request.POST.get('description')
        listAssignees = request.POST.getlist('assignees')
        listLabels = request.POST.getlist('labels')

        issue = Issue()
        issue.title = title
        issue.description = description
        issue.author = user
        issue.repository = repository

        if name != "":
            milestone = Milestone.objects.get(title=name)
            issue.milestone = milestone
            milestone.countOpenedIssues = milestone.countOpenedIssues + 1
            milestone.save()

        issue.save()

        for ass in listAssignees:
            user = User.objects.get(username=ass)
            issue.assignees.add(user)
        issue.save()

        for lab in listLabels:
            label = Label.objects.get(name=lab)
            issue.labels.add(label)
        issue.save()

        comments = Comment.objects.filter(issue=issue.pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))
        return render(request, "github/issue_view_one.html",{'issue':issue,'comments':comments,'labels':result_labels, 'milestones':milestones,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_issue_view_one(request,id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        issue = Issue.objects.get(pk=id)
        milestonesAll = Milestone.objects.all()
        milestones = []  # just opened milestones

        # comments and replies
        comments_all = Comment.objects.filter(issue=issue.pk)
        # only comments
        comments = comments_all.filter(parent=None)

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels =list(set(all_labels) - set(issue_labels))

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)

        all_history = History.objects.filter(issue=issue.pk)
        return render(request,"github/issue_view_one.html",{'issue':issue,
                                                            'comments':comments,
                                                            'labels':result_labels,
                                                            'milestones': milestones,'history':all_history,'repository':repository})

    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})

# EDIT MILESTONE IN ISSUE
def issue_edit_milestone(request, issue_id, milestone_id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        issue = Issue.objects.get(pk=issue_id)

        if issue.milestone:
            milestoneOld = issue.milestone
            if  milestoneOld.countOpenedIssues > 0:
                milestoneOld.countOpenedIssues = milestoneOld.countOpenedIssues - 1
                milestoneOld.save()

        milestone = Milestone.objects.get(pk=milestone_id)
        issue.milestone = milestone
        issue.save()

        if milestone:
            milestone.countOpenedIssues = milestone.countOpenedIssues + 1
            milestone.save()

        milestones = []
        milestonesAll = Milestone.objects.all()

        for m in milestonesAll:
            if m.repository.name == milestone.repository.name:
                if m.opened:
                    milestones.append(m)


        #comments and replies
        comments_all = Comment.objects.filter(issue=issue.pk)
        #only comments
        comments = comments_all.filter(parent=None)

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels =list(set(all_labels) - set(issue_labels))

        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html", {'issue': issue,
                                                              'comments': comments,
                                                              'labels': result_labels,
                                                              'milestones': milestones,
                                                              'history':all_history,
                                                              'repository':repository})

    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


#delete label form issue
def issue_delete_label(request,issue_id,label_id):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        issue = Issue.objects.get(pk=issue_id)
        label = Label.objects.get(pk=label_id)
        milestonesAll = Milestone.objects.all()
        milestones = []  # just opened milestones

        for m in milestonesAll:
            if m.repository.name == issue.repository.name:
                if m.opened:
                    milestones.append(m)

        # CREATE HISTORY
        history = History()
        history.description = "Label " + label.name + " deleted by " + user.username
        history.issue = issue
        history.save()

        issue.labels.remove(label)
        issue.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,
                       'comments': comments,
                       'labels': result_labels,
                       'milestones':milestones,
                       'history':all_history,
                       'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_add_label(request,issue_id,label_id):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        issue = Issue.objects.get(pk=issue_id)
        label = Label.objects.get(pk=label_id)
        milestonesAll = Milestone.objects.all()
        milestones = []  # just opened milestones

        issue.labels.add(label)
        issue.save()

        # CREATE HISTORY
        history = History()
        history.description = "Label " + label.name + " added by " + user.username
        history.issue = issue
        history.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)

        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue, 'comments': comments,
                       'labels': result_labels, 'milestones':milestones,
                       'history':all_history,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_edit_title(request,id):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        newtitle = request.POST.get('newtitle')
        issue = Issue.objects.get(pk=id)

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue.title = newtitle
        issue.save()

        # CREATE HISTORY
        history = History()
        history.description = "Title edited by " + user.username
        history.issue = issue
        history.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,'comments':comments,
                       'labels':result_labels,
                       'history':all_history,
                       'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_close(request,id):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=id)
        issue.closed = True
        issue.save()

        if issue.milestone:
            milestone = issue.milestone
            milestone.countClosedIssues = milestone.countClosedIssues + 1
            milestone.countOpenedIssues = milestone.countOpenedIssues - 1
            milestone.save()

        # CREATE HISTORY
        history = History()
        history.description = "Issue closed by " + user.username
        history.issue = issue
        history.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))
        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,'comments':comments,
                       'labels':result_labels,'history':all_history,
                        'repository': repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def issue_reopen(request,id):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=id)
        issue.closed = False
        issue.save()

        if issue.milestone:
            milestone = issue.milestone
            milestone.countClosedIssues = milestone.countClosedIssues - 1
            milestone.countOpenedIssues = milestone.countOpenedIssues + 1
            milestone.save()

        # CREATE HISTORY
        history = History()
        history.description = "Issue reopend by " + user.username
        history.issue = issue
        history.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))
        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,'comments':comments,
                       'labels':result_labels,
                       'history':all_history,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})



def comment_new(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=id)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        # CREATE COMMENT
        description = request.POST.get('comment')

        comment = Comment()
        comment.description = description
        comment.author = user
        comment.issue = issue
        comment.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)
        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,'comments':comments,
                       'labels':result_labels,'history':all_history,
                        'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def comment_edit(request, idIssue, idComment):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=idIssue)
        comment = Comment.objects.get(pk=idComment)

        newDescription = request.POST.get('comment')
        comment.description = newDescription
        comment.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))
        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue,'comments': comments,
                       'labels':result_labels,'history':all_history,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def comment_delete(request,id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=id)

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))
        all_history = History.objects.filter(issue=issue.pk)

        try:
            comment_pk = request.POST.get('commentid')
            comment = Comment.objects.get(pk=comment_pk)
            comment.delete()


            return render(request, "github/issue_view_one.html",
                          {'issue': issue,'comments': comments,
                           'messageDelete':'Comment deleted!',
                           'labels':result_labels,'history':all_history,
                           'repository': repository})
        except Comment.DoesNotExist:
            return render(request, "github/issue_view_one.html",
                          {'issue': issue, 'comments': comments,
                           'messageDelete': 'Comment deleted!',
                           'labels': result_labels, 'history': all_history,
                           'repository': repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})



def comment_reply(request, idIssue, idComment):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        issue = Issue.objects.get(pk=idIssue)
        comment = Comment.objects.get(pk=idComment)

        issue_labels = issue.labels.all()
        all_labels = Label.objects.filter(repository=repository.pk)
        result_labels = list(set(all_labels) - set(issue_labels))

        # CREATE REPLY
        replyDescription = request.POST.get('commentReply')

        reply = Comment()
        reply.description = "[reply] " + replyDescription
        reply.author = user
        reply.issue = issue
        reply.parent = comment
        reply.save()

        comments_all = Comment.objects.filter(issue=issue.pk)
        comments = comments_all.filter(parent=None)
        all_history = History.objects.filter(issue=issue.pk)
        return render(request, "github/issue_view_one.html",
                      {'issue': issue, 'comments': comments,
                       'labels':result_labels,
                       'history':all_history,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# new milestone
# name is nameRepository
def switch_milestone(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        return render(request, 'github/milestone.html', {'nameRepository': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# new milestone
# name is nameRepository
def milestone(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        date = request.POST.get('date')
        title = request.POST.get('title')
        description = request.POST.get('description')
        milestone = Milestone()
        milestone.date = date
        milestone.title = title
        milestone.description = description
        milestone.repository = Repository.objects.get(name=name)
        milestone.opened = True
        milestone.save()
        return render(request, 'github/milestoneInformation.html', {'milestone':milestone,'nameRepository': name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# name is milestoneTitle
def milestoneInfo(request, name) :
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(title=name)

        repository = Repository.objects.get(name=milestone.repository.name)

        issuesOfMilestone = []
        issuesAll = Issue.objects.all()

        for i in issuesAll.all():
            if str(i.milestone) == name:
                issuesOfMilestone.append(i)

        return render(request, 'github/milestoneInformation.html', {'milestone': milestone,
                                                                'issuesOfMilestone': issuesOfMilestone,'nameRepository':repository.name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# shows all milestones of one repository
def getAllMilestones(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestonesOfRepository = getMilestonesOfRepository(name)
        return render(request, 'github/milestonesShow.html', {'nameRepository':name,
                                                          'milestonesOfRepository': milestonesOfRepository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def getAllMilestones_open(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestones = Milestone.objects.filter(opened=True)
        milestonesOfRepository=[]
        for m in milestones:
            if m.repository.name==name:
                milestonesOfRepository.append(m)
        return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                              'milestonesOfRepository': milestonesOfRepository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def getAllMilestones_closed(request, name):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestones = Milestone.objects.filter(opened=False)
        milestonesOfRepository = []
        for m in milestones:
            if m.repository.name == name:
                milestonesOfRepository.append(m)
        return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                              'milestonesOfRepository': milestonesOfRepository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# side method
# name is repositoryName
def getMilestonesOfRepository(name):
    milestones = Milestone.objects.all()
    milestonesOfRepository = []
    for m in milestones:
        if m.repository.name == name:
            milestonesOfRepository.append(m)
    return milestonesOfRepository



def switch_label_show_all(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        labels = Label.objects.filter(repository=repository.pk)
        return render(request, "github/label_show_all.html", {'labels': labels,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_label_new(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        return render(request, "github/label_new.html",{'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def label_new(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        name = request.POST.get('name')
        color = request.POST.get('color')

        label = Label()
        label.name = name
        label.color = color
        label.repository = repository

        label.save()

        labels = Label.objects.filter(repository=repository.pk)
        return render(request, "github/label_show_all.html", {'labels': labels,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def label_edit(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        labels = Label.objects.filter(repository=repository.pk)

        label_pk = request.POST.get('label_pk')
        labelToEdit = Label.objects.get(pk=label_pk)

        #uniqie name
        new_name = request.POST.get('new_name')
        for lab in labels:
            if lab.name == new_name:
                return render(request, "github/label_show_all.html", {'labels': labels,'messageEdit':'Label name must be unique.','repository':repository})

        new_color = request.POST.get('new_color')

        labelToEdit.name = new_name
        labelToEdit.color = new_color

        labelToEdit.save()

        labels = Label.objects.filter(repository=repository.pk)
        return render(request, "github/label_show_all.html", {'labels': labels,'messageSuccess':'Label successfully changed.','repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def label_delete(request):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        label_pk = request.POST.get('label_pk')

        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        labels = Label.objects.filter(repository=repository.pk)
        try:
            label = Label.objects.get(pk=label_pk)
            label.delete()

            return render(request, "github/label_show_all.html",
                          {'labels': labels, 'messageSuccess': 'Label successfully deleted.','repository':repository})
        except Label.DoesNotExist:
            return render(request, "github/label_show_all.html",
                          {'labels': labels, 'messageSuccess': 'Label successfully deleted.','repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def create_label_from_issue(request):
    username = request.session['uname_user']
    try:
        # author
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)
        milestonesAll = Milestone.objects.all()
        milestones = []  # just opened milestones

        users = []
        if repository.members.all() is not None:
            for member in repository.members.all():
                users.append(member.username)

        #label
        name = request.POST.get('name')
        color = request.POST.get('color')

        label = Label()
        label.name = name
        label.color = color
        label.repository = repository

        label.save()

        title = request.POST.get('titleIssue')
        description = request.POST.get('descriptionIssue')
        listAssignees = request.POST.getlist('assignees')
        listLabels = request.POST.getlist('labels')

        issue = Issue()
        issue.title = title
        issue.description = description
        issue.author = user
        issue.repository = repository

        for ass in listAssignees:
            user = User.objects.get(username=ass)
            issue.assignees.add(user)

        for lab in listLabels:
            label = Label.objects.get(name=lab)
            issue.labels.add(label)

        labels = Label.objects.filter(repository=repository.pk)

        for m in milestonesAll:
            if m.repository.name == repository.name:
                if m.opened:
                    milestones.append(m)
        return render(request, "github/issue_new.html",
                      {'issue': issue, 'users': users, 'labels': labels,
                       'milestones':milestones,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def milestone_reopen(request,id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(pk=id)
        milestone.opened = True
        milestone.save()

        repository = Repository.objects.get(name=milestone.repository.name)
        return render(request, "github/milestoneInformation.html", {'milestone':milestone,'nameRepository':repository.name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def milestone_close(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(pk=id)
        milestone.opened = False
        milestone.save()

        repository = Repository.objects.get(name=milestone.repository.name)
        return render(request, "github/milestoneInformation.html", {'milestone': milestone,'nameRepository':repository.name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_milestone_edit(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(pk=id)
        repository = Repository.objects.get(name=milestone.repository.name)

        dateEdit = str(milestone.date)
        return render(request, "github/edit_milestone.html", {'dateEdit' : dateEdit,'milestone': milestone,'nameRepository':repository.name})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def milestone_edit(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(pk=id)

        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')

        milestone.title = title
        milestone.description = description
        milestone.date = date
        milestone.save()

        repository = Repository.objects.get(name=milestone.repository.name)
        milestonesOfRepository = getMilestonesOfRepository(repository.name)
        return render(request, "github/milestonesShow.html", {'milestone': milestone,'nameRepository':repository.name,
                                                              'milestonesOfRepository': milestonesOfRepository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})



def delete_milestone(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        milestone = Milestone.objects.get(pk=id)
        titleDelete = request.POST.get('titleDelete')
        name = milestone.repository.name
        if milestone.title == titleDelete:
            milestone.delete()
        else:
            return render(request, 'github/delete_milestone.html', {'nameRepository': name,'milestone':milestone, 'message': 'Title is not valid.'})
        milestonesOfRepository = getMilestonesOfRepository(name)
        return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                              'milestonesOfRepository': milestonesOfRepository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


# id is idRepository
def wiki(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository = Repository.objects.get(pk=id)
        wiki = repository.wiki
        return render(request, 'github/wiki.html', {'wiki':wiki,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def switch_wiki_edit(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        wiki = Wiki.objects.get(pk=id)
        return render(request, 'github/wiki_edit.html', {'wiki': wiki,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})


def wiki_edit(request, id):
    username = request.session['uname_user']
    try:
        user = User.objects.get(username=username)
        repository_pk = request.session['repository_id']
        repository = Repository.objects.get(pk=repository_pk)

        title = request.POST.get('title')
        content = request.POST.get('content')

        wiki = Wiki.objects.get(pk=id)
        wiki.title = title
        wiki.content = content

        wiki.save()
        repositories = Repository.objects.all()
        for r in repositories:
            if r.wiki.pk == wiki.pk:
                r.wiki = wiki
                r.save()

        return render(request, 'github/wiki.html', {'wiki':wiki,'repository':repository})
    except User.DoesNotExist:
        return render(request, "github/login.html", {'message': 'You need to login to view this content.'})
