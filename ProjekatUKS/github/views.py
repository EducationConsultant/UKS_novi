from django.shortcuts import render


from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from github.models import User, Organization, Repository, Issue, Comment, Milestone, Label, History


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
    to_email = user.email

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    return render(request, "github/activate.html", {'user':user})


# from email link to login.html
def activate_user(request,username):
    user = User.objects.get(username=username)
    user.isActive = True
    user.save()
    return render(request, "github/login.html")


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

                return render(request, "github/home.html")
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
                    "\n\n" + domain + "/github/password_reset/" + user.username +
                   "\n\n"
                   "The BooHub Team"
                   )
        to_email = user.email

        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return render(request, "github/password_reset.html", {'user':user})
    except User.DoesNotExist:
        return render(request, "github/forgot_password.html", {'message': 'User does not exist.'})


def switch_forgot_password_reset(request,username):
    request.session['uname_user'] = username
    return render(request, "github/forgot_password_reset.html",{'username':username})


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
    user = User.objects.get(username=username)
    user.loggedin = False
    user.save()

    request.session['uname_user'] = None
    request.session['loggedin'] = None
    request.session['repository_id'] = None
    return render(request, "github/login.html")

def about_user(request):
    username = request.session['uname_user']
    user = User.objects.get(username=username)

    return render(request, "github/about_user.html",{'user':user})


def switch_change_username(request):
    return render(request, "github/change_username.html")


def change_username(request):
    newusername = request.POST.get('newusername')

    username = request.session['uname_user']
    user = User.objects.get(username=username)
    user.username = newusername
    user.save()
    request.session['uname_user'] = user.username

    return render(request, "github/change_username.html", {'message': 'Username successfully changed.'})


def switch_change_password(request):
    return render(request, "github/change_password.html")


def change_password(request):
    oldpassword = request.POST.get('oldpassword')
    newpassword = request.POST.get('newpassword')
    confirmnewpassword = request.POST.get('confirmnewpassword')

    username = request.session['uname_user']
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


def switch_delete_account(request):
    return render(request, "github/delete_account.html")


def delete_account(request):
    usernameI = request.POST.get('username')
    passwordI = request.POST.get('password')

    username = request.session['uname_user']
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


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})

def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})


def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})


def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})


def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})


def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})


def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})


def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})


def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})


def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})


def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def switch_delete_organization(request, name):
    return render(request, 'github/delete_organization.html', {'name':name})


def switch_delete_repository(request, name):
    return render(request, 'github/delete_repository.html', {'name':name})


def delete_organization(request, name):
    organization = Organization.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        organization.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_organization.html', {'name': name, 'message': 'Name is not valid'})


def delete_repository(request, name):
    repository = Repository.objects.get(name=name)
    nameDelete = request.POST.get('nameDelete')
    if name == nameDelete:
        repository.delete()
        return render(request, 'github/home.html')
    else:
        return render(request, 'github/delete_repository.html', {'name': name, 'message': 'Name is not valid'})


def switch_edit_repository(request, name):
    return render(request, 'github/edit_repository.html', {'name':name})

def edit_repository(request, name):
    nameEdit = request.POST.get('nameEdit')
    repository = Repository.objects.get(name=name)
    repository.name = nameEdit
    repository.save()
    return render(request, 'github/home.html')


def switch_edit_organization(request, name):
    return render(request, 'github/edit_organization.html', {'name':name})


def edit_organization(request, name):
    nameEdit = request.POST.get('nameEdit')
    organization = Organization.objects.get(name=name)
    organization.name = nameEdit
    organization.save()
    return render(request, 'github/home.html')


def organization(request):
    organization = Organization()
    return render(request, 'github/organization.html', {'organization' : organization})


def saveOrganization(request):
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

    organization.email = email

    # put owner into members of organization
    # logged user: uname_user
    owner = request.session['uname_user']
    organization.owner = owner
    organization.save()
    for m in users:
        if m.username == owner:
            organization.members.add(m)
            organization.save()
            organizationMembers = organization.members.all

    # check if name exists
    for o in organizations:
        if o.name == name:
            return render(request, 'github/organization.html',
                          {'organization': organization,'organizationMembers': organizationMembers,'message': 'That name already exists!'})
    organization.name = name
    organization.save()

    # set nameOrganization in session
    request.session['nameOrganization'] = name

    return render(request, 'github/organizationDetails.html', {'organization':organization, 'organizationMembers': organizationMembers})


def saveOrganizationDetails(request):
    purpose = request.POST['purpose']
    howLong = request.POST['howLong']
    howMuchPeople = request.POST['howMuchPeople']

    # get nameOrganization from session
    nameOrganization = request.session['nameOrganization']

    organization = Organization()
    organizations = Organization.objects.all()
    for o in organizations:
        if o.name == nameOrganization:
            o.purpose = purpose
            o.howLong = howLong
            o.howMuchPeople = howMuchPeople
            o.save()
            organization = o
    return render(request, 'github/addNewMemberOrganization.html', {'organization': organization})


def saveOrganizationMembers(request, name):
    memberName=request.POST['member']
    organization = Organization()
    organizations = Organization.objects.all()
    users = User.objects.all()
    usernameList = []
    # find organization
    for o in organizations:
        if o.name == name:
            organization = o
    # list with all usernames
    for u in users:
        usernameList.append(u.username)
    # check username
    if memberName not in usernameList:
        return render(request, 'github/addNewMemberOrganization.html',
                      {'message': 'Username does not exist.', 'organization': organization})
    else:
        for m in users:
            if m.username == memberName:
                organization.members.add(m)
                organization.save()
                organizationMembers = organization.members.all
                return render(request, 'github/organizationInformations.html',
                              {'organization': organization, 'organizationMembers': organizationMembers})


# get all organizations by user ( owner and member)
def organizationsByUser(request):
    username = request.session['uname_user']
    organizations = Organization.objects.all()
    organizationsOfUser = []
    for o in organizations:
        for m in o.members.all():
            if m.username == username:
                organizationsOfUser.append(o)

    return render(request, 'github/organizationsShow.html', {'username': username, 'organizationsOfUser':organizationsOfUser })


# new repository
def repository(request, p):
    repository = Repository()
    return render(request, 'github/repository.html', {'repository':repository, 'p' : p})


# save new repository
def saveRepository(request, p):
    name = request.POST['name']
    description = request.POST['description']
    type = request.POST['type']
    repository = Repository()
    repository.name = name
    repository.description = description
    repository.type = type
    repository.organization = getOrganizationByName(p)
    users = User.objects.all()

    # put owner into members of repository
    # logged user: uname_user
    owner = request.session['uname_user']
    repository.owner = owner
    repository.save()
    for m in users:
        if m.username == owner:
            repository.members.add(m)
            repository.save()
            repositoryMembers = repository.members.all

    repository.save()
    return render(request, 'github/addNewMemberRepository.html', {'repository': repository, 'repositoryMembers':repositoryMembers})


# parametar 'name' is nameRepostiory
def saveRepositoryMembers(request, name):
    memberName = request.POST['member']
    repository = Repository()
    repositories = Repository.objects.all()
    users = User.objects.all()
    usernameList = []
    # find rpeository
    for r in repositories:
        if r.name == name:
            repository = r
    # list with all usernames
    for u in users:
        usernameList.append(u.username)
    # check username
    if memberName not in usernameList:
        return render(request, 'github/addNewMemberRepository.html',
                      {'message': 'Username does not exist.', 'repository': repository})
    else:
        for m in users:
            if m.username == memberName:
                repository.members.add(m)
                repository.save()
                repositoryMembers = repository.members.all
                return render(request, 'github/repositoryInformations.html',
                              {'repository': repository, 'repositoryMembers': repositoryMembers})


# shows all organisations
def organizationsShow(request):
    organizations = Organization.objects.all()
    return render(request, 'github/organizationsShow.html', {'organizations':organizations})

# informations about one organization
def organizationInfo(request, name):
    organizations = Organization.objects.all()
    organization = Organization()
    for o in organizations:
        if o.name == name:
            organization = o
    organizationMembers = organizationMembersShow(organization)
    organizationRepositories = getRepositoriesByOrganization(name)
    return render(request, 'github/organizationInformations.html', {'organization': organization,
                                                            'organizationMembers': organizationMembers,
                                                            'organizationRepositories':organizationRepositories})

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
    organization = getOrganizationByName(name)
    return render(request, 'github/addNewMemberOrganization.html', {'organization': organization})

# new member in repository, name is repositoryName
def addNewMemberRepository(request, name):
    repository = getRepositoryByName(name)
    return render(request, 'github/addNewMemberRepository.html', {'repository': repository})


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
    repositories = Repository.objects.all()
    repositoriesOfUser = []
    for o in repositories:
        for m in o.members.all():
            if m.username == username:
                repositoriesOfUser.append(o)

    return render(request, 'github/repositoriesShow.html', {'username': username, 'repositoriesOfUser':repositoriesOfUser })


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
                                                                    'repositoryMembers': repositoryMembers,
                                                                    })


def switch_issue_show_all(request):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    issues = Issue.objects.filter(repository=repository.pk)
    return render(request, "github/issue_show_all.html",{'issues':issues})


def issue_show_all_open(request):
    issues = Issue.objects.filter(closed=False)
    return render(request, "github/issue_show_all.html",{'issues': issues})


def issue_show_all_closed(request):
    issues = Issue.objects.filter(closed=True)
    return render(request, "github/issue_show_all.html",{'issues': issues})


def switch_issue_new(request):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    users=[]
    if repository.members.all() is not None:
        for member in repository.members.all():
            users.append(member.username)

    labels = Label.objects.filter(repository=repository.pk)
    return render(request, "github/issue_new.html", {'users':users,'labels':labels})


def issue_new(request):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    title = request.POST.get('title')
    description = request.POST.get('description')
    listAssignees = request.POST.getlist('assignees')
    listLabels = request.POST.getlist('labels')

    username = request.session['uname_user']
    user = User.objects.get(username=username)

    issue = Issue()
    issue.title = title
    issue.description = description
    issue.author = user
    issue.repository = repository

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
    return render(request, "github/issue_view_one.html",{'issue':issue,'comments':comments,'labels':result_labels})


def switch_issue_view_one(request,id):
    issue = Issue.objects.get(pk=id)

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
    return render(request,"github/issue_view_one.html",{'issue':issue,'comments':comments,'labels':result_labels, 'history':all_history})


#delete label form issue
def issue_delete_label(request,issue_id,label_id):
    issue = Issue.objects.get(pk=issue_id)
    label = Label.objects.get(pk=label_id)

    # author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
                  {'issue': issue, 'comments': comments, 'labels': result_labels, 'history':all_history})


def issue_add_label(request,issue_id,label_id):
    issue = Issue.objects.get(pk=issue_id)
    label = Label.objects.get(pk=label_id)

    issue.labels.add(label)
    issue.save()

    # author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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

    all_history = History.objects.filter(issue=issue.pk)
    return render(request, "github/issue_view_one.html",
                  {'issue': issue, 'comments': comments, 'labels': result_labels, 'history':all_history})


def issue_edit_title(request,id):
    newtitle = request.POST.get('newtitle')
    issue = Issue.objects.get(pk=id)

    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    issue.title = newtitle
    issue.save()

    # author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_view_one.html", {'issue': issue,'comments':comments,'labels':result_labels,'history':all_history})


def issue_close(request,id):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    issue = Issue.objects.get(pk=id)
    issue.closed = True
    issue.save()

    # author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_view_one.html", {'issue': issue,'comments':comments,'labels':result_labels,'history':all_history})


def issue_reopen(request,id):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    issue = Issue.objects.get(pk=id)
    issue.closed = False
    issue.save()

    # author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_view_one.html", {'issue': issue,'comments':comments,'labels':result_labels,'history':all_history})


def comment_new(request, id):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_view_one.html", {'issue': issue,'comments':comments,'labels':result_labels,'history':all_history})


def comment_edit(request, idIssue, idComment):
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
    return render(request, "github/issue_view_one.html", {'issue': issue,'comments': comments,'labels':result_labels,'history':all_history})

def comment_delete(request,id):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    issue = Issue.objects.get(pk=id)

    comment_pk = request.POST.get('commentid')
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()

    comments_all = Comment.objects.filter(issue=issue.pk)
    comments = comments_all.filter(parent=None)

    issue_labels = issue.labels.all()
    all_labels = Label.objects.filter(repository=repository.pk)
    result_labels = list(set(all_labels) - set(issue_labels))
    all_history = History.objects.filter(issue=issue.pk)
    return render(request, "github/issue_view_one.html",{'issue': issue,'comments': comments,'messageDelete':'Comment deleted!','labels':result_labels,'history':all_history})


def comment_reply(request, idIssue, idComment):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_view_one.html", {'issue': issue, 'comments': comments,'labels':result_labels,'history':all_history})

# new milestone
# name is nameRepository
def switch_milestone(request, name):
    return render(request, 'github/milestone.html', {'nameRepository': name})

# new milestone
# name is nameRepository
def milestone(request, name):
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
    return render(request, 'github/milestoneInformation.html', {'milestone':milestone})

# name is milestoneName
def milestoneInfo(request, name ) :
    milestone = Milestone.objects.get(title=name)
    return render(request, 'github/milestoneInformation.html', {'milestone': milestone})

# shows all milestones of one repository
def getAllMilestones(request, name):
    milestonesOfRepository = getMilestonesOfRepository(name)
    return render(request, 'github/milestonesShow.html', {'nameRepository':name,
                                                          'milestonesOfRepository': milestonesOfRepository})


def getAllMilestones_open(request, name):
    milestones = Milestone.objects.filter(opened=True)
    milestonesOfRepository=[]
    for m in milestones:
        if m.repository.name==name:
            milestonesOfRepository.append(m)
    return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                          'milestonesOfRepository': milestonesOfRepository})


def getAllMilestones_closed(request, name):
    milestones = Milestone.objects.filter(opened=False)
    milestonesOfRepository = []
    for m in milestones:
        if m.repository.name == name:
            milestonesOfRepository.append(m)
    return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                          'milestonesOfRepository': milestonesOfRepository})


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
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

    labels = Label.objects.filter(repository=repository.pk)
    return render(request, "github/label_show_all.html", {'labels': labels})

def switch_label_new(request):
    return render(request, "github/label_new.html")

def label_new(request):
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
    return render(request, "github/label_show_all.html", {'labels': labels})

def label_edit(request):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)
    labels = Label.objects.filter(repository=repository.pk)

    label_pk = request.POST.get('label_pk')
    labelToEdit = Label.objects.get(pk=label_pk)

    #uniqie name
    new_name = request.POST.get('new_name')
    for lab in labels:
        if lab.name == new_name:
            return render(request, "github/label_show_all.html", {'labels': labels,'messageEdit':'Label name must be unique.'})

    new_color = request.POST.get('new_color')

    labelToEdit.name = new_name
    labelToEdit.color = new_color

    labelToEdit.save()

    labels = Label.objects.filter(repository=repository.pk)
    return render(request, "github/label_show_all.html", {'labels': labels,'messageSuccess':'Label successfully changed.'})

def label_delete(request):
    label_pk = request.POST.get('label_pk')
    label = Label.objects.get(pk=label_pk)

    label.delete()

    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)
    labels = Label.objects.filter(repository=repository.pk)
    return render(request, "github/label_show_all.html",
                  {'labels': labels, 'messageSuccess': 'Label successfully deleted.'})

def create_label_from_issue(request):
    repository_pk = request.session['repository_id']
    repository = Repository.objects.get(pk=repository_pk)

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

    #author
    username = request.session['uname_user']
    user = User.objects.get(username=username)

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
    return render(request, "github/issue_new.html",
                  {'issue': issue, 'users': users, 'labels': labels})

def milestone_reopen(request,id):
    milestone = Milestone.objects.get(pk=id)
    milestone.opened = True
    milestone.save()
    return render(request, "github/milestoneInformation.html", {'milestone':milestone})


def milestone_close(request, id):
    milestone = Milestone.objects.get(pk=id)
    milestone.opened = False
    milestone.save()
    return render(request, "github/milestoneInformation.html", {'milestone': milestone})

def switch_milestone_edit(request, id):
    milestone = Milestone.objects.get(pk=id)
    print("*******************" + str(milestone.date))
    dateEdit = str(milestone.date)
    return render(request, "github/edit_milestone.html", {'dateEdit' : dateEdit,'milestone': milestone})

def milestone_edit(request, id):
    milestone = Milestone.objects.get(pk=id)
    title = request.POST.get('title')
    description = request.POST.get('description')
    date = request.POST.get('date')
    milestone.title = title
    milestone.description = description
    milestone.date = date
    milestone.save()
    return render(request, "github/milestoneInformation.html", {'milestone': milestone})



def delete_milestone(request, id):
    milestone = Milestone.objects.get(pk=id)
    name = milestone.repository.name
    milestone.delete()
    milestonesOfRepository = getMilestonesOfRepository(name)
    return render(request, 'github/milestonesShow.html', {'nameRepository': name,
                                                          'milestonesOfRepository': milestonesOfRepository})




