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
    howLong =  models.CharField(max_length=50)
    howMuchPeople =  models.CharField(max_length=50)
    members = models.ManyToManyField(User)
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
