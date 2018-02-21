from django.db import models
#from django.test import TestCase
import unittest

#from . import models


class MyTest(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(3, 4)

    def test_list(self):
        print('**************************************************')

        testList = [1, 2, 3]
        value = [4,5,6]

        self.assertListEqual(testList,value)

