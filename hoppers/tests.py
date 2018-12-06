import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Hopper

class HopperTestCase(TestCase):

    def create_anonymous_hopper(self):
        print("Creating anonymous hopper model...")
        user_instance = User.objects.create(username='jon', password='drew')
        anonymous_hopper_instance = user_instance.hopper
        return anonymous_hopper_instance

    def test_hopper_creation(self):
        print("Testing if creating a user automatically generates a hopper...")
        test_instance = self.create_anonymous_hopper()

        self.assertIsInstance(test_instance, Hopper)

    def test_hopper_is_anonymous(self):
        print("Testing if the hopper created when providing only username and password is anonymous...")
        test_instance = self.create_anonymous_hopper()
        is_anonymous = test_instance.anonymous

        self.assertIs(is_anonymous, True)

    def test_hopper_get_fields_method(self):
        print("Testing the hopper get_fields method...")
        test_instance = self.create_anonymous_hopper()
        test_instance_fields = test_instance.get_fields()
        counter = 0
        for field in test_instance_fields:
          counter += 1

        self.assertEqual(counter, 10)

    def test_hopper_get_absolute_url_method(self):
        print("Testing the hopper get_absolute_url method...")
        test_instance = self.create_anonymous_hopper()
        test_instance_url = test_instance.get_absolute_url()

        self.assertEqual(test_instance_url[:23], '/hoppers/' + test_instance.slug)






