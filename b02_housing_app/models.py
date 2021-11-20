from django.db import models


class Apartment(models.Model):
    field_dict = {
        "apt_price": "Monthly rent($)",
        "apt_area": "Area (sq ft)",
        "apt_beds": "Number of beds",
        "apt_baths": "Number of baths",
        "apt_lease": "Lease length (in months)",
        "apt_deposit": "Deposit($)",
        "apt_movein": "Move-in date",
    }
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
        return self.apt_name
    @staticmethod
    def field_desc(field_name):
        return Apartment.field_dict[field_name]
    def get_valid_fields(self):
        valid_fields = []
        for field_name in Apartment.field_dict.keys():
            if self.__getattribute__(field_name) is not None:
                valid_fields.append(field_name)
        return valid_fields


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
