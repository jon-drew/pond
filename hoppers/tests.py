from django.test import TestCase
from .models import Hopper
from django.contrib.auth.models import User

class HopperTestCase(TestCase):

    def setUp(self):
        Hopper.objects.create(user=User.objects.create_user(username="mike"))
        Hopper.objects.create(user=User.objects.create_user(username="smith"), name="meow")

    # def test_hopper_fields(self):
    #     Hopper.objects.get_fields()