from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Apartment, Review


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

    #Tests if logout works
    def test_signout(self):
        cl = Client()
        cl.login(username='dummyUser', password='TestPassword1?')
        User = get_user_model()
        user = User.objects.get(username = 'dummyUser')
        cl.logout()
        self.assertFalse(user.is_anonymous)

    #Does not login if user doesn't exist
    def test_nouser(self):
        cl = Client()
        self.assertFalse(cl.login(username='dumbUser', password='TestPassword1@'))

class PropertyListingTest(TestCase):
    
    #Creates a normal user, no need just need something here
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='dummyUser')
        user.set_password('TestPassword1?')
        user.save()

    #Check if property can be added
    def test_addproperty(self):
        Apartment.objects.create(apt_name='DummyApt')
        self.assertTrue(Apartment.objects.filter(apt_name='DummyApt').exists())
    
    #Check if review can be added
    def test_addreview(self):
        apartment = Apartment(apt_name='DummyApt')
        apartment.save()
        review = Review(apt_name=apartment,apt_stars=1)
        review.save()
        self.assertTrue(Review.objects.filter(apt_name=apartment).exists())
    
    #Check if property can be removed
    def test_removeproperty(self):
        Apartment.objects.create(apt_name='DummyApt')
        Apartment.objects.filter(apt_name='DummyApt').delete()
        self.assertFalse(Apartment.objects.filter(apt_name='DummyApt').exists())
    
    #Check if review can be removed
    def test_removereview(self):
        apartment = Apartment(apt_name='DummyApt')
        apartment.save()
        review = Review(apt_name=apartment,apt_stars=1)
        review.save()
        Review.objects.filter(apt_name=apartment).delete()
        self.assertFalse(Review.objects.filter(apt_name=apartment).exists())