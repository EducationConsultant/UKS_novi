from django.shortcuts import render


from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site

from github.models import User, Organization, Issue


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
        if user.password == password:
            user.loggedin = True
            user.save()

            request.session['uname_user'] = user.username
            request.session['loggedin'] = 'True'

            return render(request, "github/home.html")
        else:
            return render(request, "github/login.html",{'message':'Incorrect password.','uname':username})
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
            return render(request, "github/delete_account.html", {'message': 'Password is not valid.'})
    else:
        return render(request, "github/delete_account.html", {'message': 'Username is not valid.'})

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

def switch_issue_show_all(request):
    issues = Issue.objects.all()
    return render(request, "github/issue_show_all.html",{'issues':issues})


def issue_show_all_open(request):
    issues = Issue.objects.filter(closed=False)
    return render(request, "github/issue_show_all.html",{'issues': issues})


def issue_show_all_closed(request):
    issues = Issue.objects.filter(closed=True)
    return render(request, "github/issue_show_all.html",{'issues': issues})


def switch_issue_new(request):
    #TODO: dodaj listu svih korisnika koji su na tom repozitorijumu na kom se kreira problem
    #ovo je potrebno zbog asssignees
    users = User.objects.all()
    return render(request, "github/issue_new.html", {'users':users})


def issue_new(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    listAsssignees = request.POST.getlist('asssignees')

    username = request.session['uname_user']
    user = User.objects.get(username=username)

    issue = Issue()
    issue.title = title
    issue.description = description
    issue.creator = user

    issue.save()

    for ass in listAsssignees:
        user = User.objects.get(username=ass)
        issue.asssignees.add(user)
    issue.save()

    users = User.objects.all()
    return render(request, "github/issue_new.html",{'message':'Issue successfully created.','users':users})


def switch_issue_view_one(request,id):
    issue = Issue.objects.get(pk=id)
    return render(request,"github/issue_view_one.html",{'issue':issue})


def issue_edit_title(request,id):
    newtitle = request.POST.get('newtitle')
    issue = Issue.objects.get(pk=id)

    issue.title = newtitle
    issue.save()
    return render(request, "github/issue_view_one.html", {'issue': issue})


def issue_close(request,id):
    issue = Issue.objects.get(pk=id)
    issue.closed = True
    issue.save()

    return render(request, "github/issue_view_one.html", {'issue': issue})


def issue_reopen(request,id):
    issue = Issue.objects.get(pk=id)
    issue.closed = False
    issue.save()

    return render(request, "github/issue_view_one.html", {'issue': issue})




