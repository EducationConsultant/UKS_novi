from django.test import TestCase



class AnimalTestCase(TestCase):

    def test_animals_can_speak(self):
        self.assertEqual(2, 2)


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
        self.assertEqual(self.organziation.purpose,"Educational purposes" )
        self.assertEqual(self.organization.howLong, "Indefinitely")
        self.asserrtEqual(self.organization.howMuchPeople, "5 or fewer")
        self.assertEqueal(self.organization.owner, self.user)

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
        self.assertEqual(self.repository.type, "private")
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
        assertEqual(self.repository.name, "repo123")


class MilestoneTestCase(TestCase):
    def setUp(self):
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