from django.db import models


# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=80)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    isActive = models.BooleanField(default=False)
    loggedin = models.BooleanField(default=False)

    def __str__(self):
        return self.firstname + " " + self.lastname + " " + self.username + " " + self.email


class Organization(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    howLong = models.CharField(max_length=50)
    howMuchPeople = models.CharField(max_length=50)
    members = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    purposeList = {'Professional work, for-profit',
                   'Professional work, for-non-profit',
                   'Educational purposes',
                   'An open source project',
                   'Other'
    }
    howLongList = { 'Just a few days',
                    'A few weeks to months',
                    ' year or more',
                    'Indefinitely',
                    'Other',
    }
    howMuchPeopleList = { 'I plan to work alone',
                          '5 or fewer',
                          '6 to 20',
                          'Other'

    }

    def __str__(self):
        return self.name

class Wiki(models.Model):
    content = models.TextField(null=True)
    title = models.CharField(null=True, max_length = 100)

    def __str__(self):
        return self.content

class Repository(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.CharField( max_length=50)
    typeList = {'private', 'public'}
    members = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_repository')
    wiki = models.OneToOneField(Wiki, null=True,on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.color


class Milestone(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    opened = models.BooleanField(default=True)
    countOpenedIssues = models.PositiveIntegerField(default=0)
    countClosedIssues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class Issue(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assignees = models.ManyToManyField(User, related_name='assignees')
    closed = models.BooleanField(default=False)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)
    milestone = models.ForeignKey(Milestone, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.title + " " + self.description


class Comment(models.Model):
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE,related_name='replies')

    def __str__(self):
        return self.author + " " + self.description


class History(models.Model):
    description = models.CharField(max_length=500)
    createdDate = models.DateTimeField(auto_now=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.description + " " + self.createdDate

