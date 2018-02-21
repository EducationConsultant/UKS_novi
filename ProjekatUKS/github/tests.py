from django.db import models
#from django.test import TestCase
import unittest

#from . import models


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(firstname="Djole", lastname="Pingvin", username="pingvin_djole",
                            password="djole123", email="djole@gmail.com",
                            isActive=True, loggedin=False)

    def test_login_user(self):
        self.user.loggedin = True
        self.user.save()

        self.assertTrue(self.user.loggedin)

    def test_logout(self):
        self.user.loggedin = False
        self.user.save()

        self.assertFalse(self.user.loggedin)

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
