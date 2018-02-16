from django.db import models
import datetime


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
    howLong =  models.CharField(max_length=50)
    howMuchPeople =  models.CharField(max_length=50)
    members = models.ManyToManyField(User)
    owner = models.CharField(max_length=50)
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


class Repository(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.CharField( max_length=50)
    typeList = {'private', 'public'}
    members = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    owner = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.color


class Issue(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assignees = models.ManyToManyField(User, related_name='assignees')
    closed = models.BooleanField(default=False)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.title + " " + self.description


class Comment(models.Model):
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    createdDate = models.DateField(("Date"), default=datetime.date.today)
    reply = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='comment')
    replies = []
    isReply = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Milestone(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
