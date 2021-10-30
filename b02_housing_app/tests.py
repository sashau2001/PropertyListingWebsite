from django.test import TestCase, Client
from django.contrib.auth import get_user_model



class DummyTest(TestCase):
    def test_dummy(self):
        self.assertTrue(True)

class LoginTest(TestCase):
    
    #Create dummy user for tests
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='dummyUser')
        user.set_password('TestPassword1?')
        user.save()

    #Tests login when user exists
    def test_exists(self):
        cl = Client()
        exists = cl.login(username='dummyUser', password='TestPassword1?')
        self.assertTrue(exists)