from django.db import models
from django.test import TestCase

from ..models import User


class ProbaTestCase(TestCase):
	def test_proba(self):
		self.assertEsqual(2,4)

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname ="User", lastname="User",
                                        username="user", password="user",
                                        email="user@gmail.com", isActive = True, loggedin = True)

        self.member = User.objects.create(firstname="Member", lastname="Member",
                                        username="member", password="member",
                                        email="member@gmail.com", isActive=True, loggedin=True)

        self.organization = Organization.objects.create(name="org", email ="org@gmail.com",
                                    purpose="Educational purposes", howLong="Indefinitely",
                                    howMuchPeople = "5 or fewer", owner = self.user)

    def test_organization_add_new(self):
        self.assertEqual(self.organization.name, "org")
        self.assertEqual(self.organization.email, "org@gmail.com")
        self.assertEqual(self.organization.purpose,"Educational purposes" )
        self.assertEqual(self.organization.howLong, "Indefinitely")
        self.assertEqual(self.organization.howMuchPeople, "5 or fewer")
        self.assertEqual(self.organization.owner, self.user)

    def test_organization_addNewMemberOrganization(self):
        self.organization.members.add(self.member)
        self.organization.members.add(self.user)
        self.organization.save()
        self.assertEqual(len(self.organization.members.all()), 2)

    def test_organization_edit(self):
        newName = "org123"
        self.organization.name = newName
        self.organization.save()
        self.assertEqual(self.organization.name, newName)


class RepositoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname ="User", lastname="User",
                                        username="user", password="user",
                                        email="user@gmail.com", isActive = True, loggedin = True)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.user)

        self.member = User.objects.create(firstname="Member", lastname="Member",
                                      username="member", password="member",
                                      email="member@gmail.com", isActive=True, loggedin=True)

        self.member2 = User.objects.create(firstname="Member2", lastname="Member2",
                                          username="member2", password="member2",
                                          email="member2@gmail.com", isActive=True, loggedin=True)

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization = self.organization,
                                                    owner = self.user)

    def test_repository_add_new(self):
        self.assertEqual(self.repository.name, "repo")
        self.assertEqual(self.repository.description, "Student's repository")
        self.assertEqual(self.repository.type, "public")
        self.assertEqual(self.repository.organization.name, "org")
        self.assertEqual(self.repository.owner, self.user)

    def test_repository_addNewMemberRepository(self):
        self.repository.members.add(self.member)
        self.repository.members.add(self.member2)
        self.repository.members.add(self.user)
        self.repository.save()
        self.assertEqual(len(self.repository.members.all()), 3)

    def test_repository_edit(self):
        newName = "repo123"
        self.repository.name = newName
        self.repository.save()
        self.assertEqual(self.repository.name, "repo123")


class MilestoneTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname="User", lastname="User",
                                        username="user", password="user",
                                        email="user@gmail.com", isActive=True, loggedin=True)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.user)

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization=self.organization,
                                                    owner=self.user)

        self.milestone = Milestone.objects.create(date="2018-02-19",
                                                  title = "Milestone 1",
                                                  description = "Milestone for study",
                                                  repository = self.repository,
                                                  opened = True)
    def test_milestone_add_new(self):
        self.assertEqual(self.milestone.date, "2018-02-19")
        self.assertEqual(self.milestone.title, "Milestone 1")
        self.assertEqual(self.milestone.description, "Milestone for study")
        self.assertEqual(self.milestone.repository, self.repository)
        self.assertEqual(self.milestone.opened, True)

    def test_milestone_close(self):
        self.milestone.opened = False
        self.milestone.save()
        self.assertEqual(self.milestone.opened, False)

    def test_milestone_reopen(self):
        self.milestone.opened = True
        self.milestone.save()
        self.assertEqual(self.milestone.opened, True)

    def test_milestone_edit(self):
        newTitle = "Mileston"
        self.milestone.title = newTitle
        self.assertEqual(self.milestone.title, "Mileston")


class WikiTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(firstname="User", lastname="User",
                                        username="user", password="user",
                                        email="user@gmail.com", isActive=True, loggedin=True)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.user)

        self.wiki = Wiki.objects.create(title="Wiki page", content="Wiki is about my repository...")

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization=self.organization,
                                                    owner=self.user, wiki = self.wiki)

    def test_wiki_edit(self):
        newTitle = "New title"
        newContent = "New content"
        self.wiki.title = newTitle
        self.wiki.content = newContent
        self.wiki.save()
        self.assertEqual(self.wiki.title, "New title")
        self.assertEqual(self.wiki.content, "New content")


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname="Djole", lastname="Pingvin", username="pingvin_djole",
                            password="djole123", email="djole@gmail.com",
                            isActive=True, loggedin=False)

    def test_login_user(self):
        self.user.loggedin = True
        self.user.save()

        self.assertEqual(self.user.loggedin, True)

    def test_logout(self):
        self.user.loggedin = False
        self.user.save()

        self.assertEqual(self.user.loggedin, False)

    def test_change_username(self):
        new_username = "new_username"

        self.user.username = new_username
        self.user.save()

        self.assertEqual(self.user.username, "new_username")

    def test_change_password(self):
        old_password = "djole123"
        self.assertEqual(self.user.password, old_password)

        new_password = "newpass123"
        confirm_new_password = "newpass123"
        self.assertEqual(new_password, confirm_new_password)

        self.user.password = new_password
        self.user.save()
        self.assertEqual(self.user.password, new_password)


class LabelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname="Djole", lastname="Pingvin", username="pingvin_djole",
                            password="djole123", email="djole@gmail.com",
                            isActive=True, loggedin=False)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.user)

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization=self.organization,
                                                    owner=self.user)

        self.label = Label.objects.create(name="red", color="#ff1a1a", repository=self.repository)


    def test_label_new(self):
        self.assertEqual(self.label.name, "red")


    def test_label_edit(self):
        new_name = "yellow"
        new_color = "#ffff1a"

        self.label.name = new_name
        self.label.color = new_color
        self.label.save()

        self.assertEqual(self.label.name, new_name)
        self.assertEqual(self.label.color, new_color)


class IssueTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(firstname="Djole", lastname="Pingvin", username="pingvin_djole",
                            password="djole123", email="djole@gmail.com",
                            isActive=True, loggedin=False)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.author)

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization=self.organization,
                                                    owner=self.author)

        self.label = Label.objects.create(name="red", color="#ff1a1a", repository=self.repository)

        self.milestone = Milestone.objects.create(date="2018-02-19",
                                                  title="Milestone 1",
                                                  description="Milestone for study",
                                                  repository=self.repository,
                                                  opened=True)

        self.issue = Issue.objects.create(title="Issue 1", description="Description",
                                          author=self.author, closed=False,
                                          repository=self.repository,
                                          milestone=self.milestone)


    def test_issue_new(self):
        self.assertEqual(self.issue.title, "Issue 1")
        self.assertEqual(self.issue.description, "Description")


    def test_edit_issue(self):
        new_title = "New title"
        self.issue.title = new_title
        self.issue.save()

        self.assertEqual(self.issue.title, new_title)


    def test_issue_close(self):
        self.issue.closed = True
        self.issue.save()

        self.assertEqual(self.issue.closed, True)


    def test_issue_reopen(self):
        self.issue.closed = False
        self.issue.save()

        self.assertEqual(self.issue.closed, False)

class CommentTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(firstname="Djole", lastname="Pingvin", username="pingvin_djole",
                            password="djole123", email="djole@gmail.com",
                            isActive=True, loggedin=False)

        self.organization = Organization.objects.create(name="org", email="org@gmail.com",
                                                        purpose="Educational purposes", howLong="Indefinitely",
                                                        howMuchPeople="5 or fewer", owner=self.author)

        self.repository = Repository.objects.create(name="repo", description="Student's repository",
                                                    type="public", organization=self.organization,
                                                    owner=self.author)

        self.label = Label.objects.create(name="red", color="#ff1a1a", repository=self.repository)

        self.milestone = Milestone.objects.create(date="2018-02-19",
                                                  title="Milestone 1",
                                                  description="Milestone for study",
                                                  repository=self.repository,
                                                  opened=True)

        self.issue = Issue.objects.create(title="Issue 1", description="Description",
                                          author=self.author, closed=False,
                                          repository=self.repository,
                                          milestone=self.milestone)

        self.comment = Comment.objects.create(description="Description",author=self.author,
                                              issue=self.issue)


    def test_comment_new(self):
        self.assertEqual(self.comment.description, "Description")


    def test_comment_edit(self):
        new_desciption = "new description"
        self.comment.description = new_desciption
        self.comment.save()

        self.assertEqual(self.comment.description, new_desciption)


    def test_comment_reply(self):
        self.reply = Comment.objects.create(description="Reply description", author=self.author,
                                              issue=self.issue,parent=self.comment)

        self.assertEqual(self.reply.parent.description, "Description")


