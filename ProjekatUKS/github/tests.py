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
        self.organization.save()
        self.assertEqueal(len(self.organization.members.all()), 1)