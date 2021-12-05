from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomTemplate:
    field_dict = {}

    @classmethod
    def field_desc(cls,field_name):
        return cls.field_dict[field_name]

    def get_valid_fields(self):
        cls = self.__class__
        valid_fields = []
        for field_name in cls.field_dict.keys():
            if self.__getattribute__(field_name) is not None:
                valid_fields.append(field_name)
        return valid_fields

class Apartment(models.Model,CustomTemplate):
    field_dict = {
        "apt_price": "Monthly rent($)",
        "apt_area": "Area (sq ft)",
        "apt_beds": "Number of beds",
        "apt_baths": "Number of baths",
        "apt_lease": "Lease length (in months)",
        "apt_deposit": "Deposit($)",
        "apt_movein": "Move-in date",
    }
    id = models.BigAutoField(primary_key=True)
    apt_name = models.CharField(max_length=100)
    apt_location = models.TextField()
    apt_area = models.IntegerField(null=True,blank=True) # square feet
    apt_price = models.IntegerField(null=True,blank=True) # in US dollars
    apt_beds = models.IntegerField(null=True,blank=True)
    apt_baths = models.DecimalField(max_digits=2,decimal_places=1,null=True,blank=True)
    apt_lease = models.IntegerField(null=True,blank=True) # months
    apt_deposit = models.IntegerField(null=True,blank=True) # in US dollars
    apt_movein = models.DateField(null=True,blank=True)
    def __str__(self):
        if hasattr(self,'dist'): # for search results
            return "{} ({:.1f} km)".format(self.apt_name, self.dist/1000) # Apartment (3.2 km)
        return self.apt_name


class Review(models.Model):
    apt_name = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    apt_reviewer = models.CharField(max_length=100)
    apt_review = models.TextField()
    class Stars(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    apt_stars = models.IntegerField(choices=Stars.choices)

    def __str__(self):
        return "\"{}\" by \"{}\"".format(self.apt_name,self.apt_reviewer)

class Profile(models.Model, CustomTemplate):
    field_dict = {
        "public_username": "Username",
        "bio": "Bio",
        "searching_for_apt": "Searching For Apartment?",
        "price_range_min": "Minimum rent",
        "price_range_max": "Maximum rent",
        "desired_movein_min": "Earliest move-in date",
        "desired_movein_max": "Latest move-in date",
        "desired_beds_min": "Minimum bedrooms",
        "desired_beds_max": "Maximum bedrooms"
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_username = models.CharField(max_length=20)
    bio = models.CharField(max_length=300,null=True,blank=True)
    searching_for_apt = models.BooleanField(default=True,blank=True)
    price_range_min = models.IntegerField(null=True,blank=True)
    price_range_max = models.IntegerField(null=True,blank=True)
    desired_movein_min = models.DateField(null=True,blank=True)
    desired_movein_max = models.DateField(null=True,blank=True)
    desired_beds_min = models.IntegerField(null=True,blank=True)
    desired_beds_max = models.IntegerField(null=True,blank=True)
