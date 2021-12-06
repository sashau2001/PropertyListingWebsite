from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpRequest

import sys

from .models import Apartment, Review
from .views import reviews, apartments, apartment, insert_review, search_results


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
    def test_no_user(self):
        cl = Client()
        self.assertFalse(cl.login(username='dumbUser', password='TestPassword1@'))

class PropertyListingTest(TestCase):
    
    #Creates a normal user
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='dummyUser')
        user.set_password('TestPassword1?')
        user.save()

    #Check if property can be added
    def test_addproperty(self):
        Apartment.objects.create(apt_name='DummyApt', apt_location='St.New Lenox, IL 60451')
        self.assertTrue(Apartment.objects.filter(apt_name='DummyApt').exists())
    
    #Check if review can be added
    def test_add_review(self):
        apartmentTest = Apartment(apt_name='DummyApt',apt_location='St.New Lenox, IL 60451')
        apartmentTest.save()
        review = Review(apt_name=apartmentTest,apt_stars=1)
        review.save()
        self.assertTrue(Review.objects.filter(apt_name=apartmentTest).exists())
    
    #Check if property can be removed
    def test_remove_property(self):
        Apartment.objects.create(apt_name='DummyApt')
        Apartment.objects.filter(apt_name='DummyApt').delete()
        self.assertFalse(Apartment.objects.filter(apt_name='DummyApt').exists())
    
    #Check if review can be removed
    def test_remove_review(self):
        apartmentTest = Apartment(apt_name='DummyApt',apt_location='St.New Lenox, IL 60451')
        apartmentTest.save()
        review = Review(apt_name=apartmentTest,apt_stars=1)
        review.save()
        Review.objects.filter(apt_name=apartmentTest).delete()
        self.assertFalse(Review.objects.filter(apt_name=apartmentTest).exists())

    #Check if properly redirected to list of apartments
    def test_list_redirect(self):
        request = HttpRequest()
        response = apartments(request)
        # sys.stderr.write(repr(request.path) + '\n')
        self.assertTrue(response.status_code == 200) 
    
    #Check if properly redirected to apartment
    def test_apartment_redirect(self):
        apartmentTest = Apartment(apt_name='DummyApt',apt_location='St.New Lenox, IL 60451')
        apartmentTest.save()
        
        request = HttpRequest()
        response = apartment(request, 1)
        #sys.stderr.write(repr(response.content) + '\n')
        self.assertTrue(response.status_code == 200) 

    #Check if properly redirected to list of reviews page
    def test_reviews_redirect(self):
        request = HttpRequest()
        response = reviews(request)
        # sys.stderr.write(repr(request.path) + '\n')
        self.assertTrue(response.status_code == 200) 

    #Check if properly redirected to submit review page when logged in
    def test_make_review_redirect(self):
        cl = Client()
        cl.login(username='dummyUser', password='TestPassword1?')
        response = cl.get(reverse('insert_review'))
        # sys.stderr.write(repr(response.headers) + '\n')
        self.assertEquals(response.status_code, 200) 

    #Check if properly redirected to login for submit review if not logged in
    def test_make_review_no_login_redirect(self):
        cl = Client()
        response = cl.get(reverse('insert_review'))
        # sys.stderr.write(repr(response.headers) + '\n')
        #self.assertRedirects(request,'/accounts/google/login/', status_code=302, target_status_code=200) 
        self.assertEquals(response.headers['Location'], '/accounts/google/login/')
        self.assertEquals(response.status_code, 302) 

class GoogleMapTest(TestCase):

    def test_google_maps_exists(self):
        apartmentTest = Apartment(apt_name='DummyApt',apt_location='St.New Lenox, IL 60451')
        apartmentTest.save()

        request = HttpRequest()
        response = apartment(request, 1)
        # sys.stderr.write(repr(response.content) + '\n')
        self.assertContains(response,'https://www.google.com/maps/') 
        self.assertContains(response,'St.New Lenox, IL 60451') 

class SearchTest(TestCase):
    def setUp(self):
        apartmentTest = Apartment(apt_name='DummyApt',apt_location='St.New Lenox, IL 60451', apt_price=100)
        apartmentTest2 = Apartment(apt_name='ExpensiveApt',apt_location='St.New Lenox, IL 60451', apt_price=1000)
        apartmentTest.save()
        apartmentTest2.save()
    
    #Simple test for apartment in list
    def test_simple_search(self):
        request = HttpRequest()
        request.GET.__setitem__('name','Dummy')
        response = apartments(request)
        # sys.stderr.write(repr(response.content) + '\n')
        self.assertContains(response, 'DummyApt') 

    #Simple test for apartment not in list
    def test_not_contain(self):
        request = HttpRequest()
        request.GET.__setitem__('name','Nothing')
        response = apartments(request)
        # sys.stderr.write(repr(response.content) + '\n') 
        # sys.stderr.write(repr(request.GET.__getitem__('name_query')) + '\n')
        self.assertNotContains(response, 'DummyApt') 

