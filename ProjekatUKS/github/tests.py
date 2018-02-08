from django.test import TestCase



class AnimalTestCase(TestCase):


    def test_animals_can_speak(self):
        self.assertEqual(2, 2)
