from django.db import models
from enum import Enum

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
    def __str__(self):
        return self.name


class Issue(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_issue')
    asssignees = models.ManyToManyField(User, related_name='assignees_issue')
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " " + self.description

