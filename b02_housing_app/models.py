from django.db import models


class Apartment(models.Model):
    # Treat -1 as NULL
    apt_name = models.CharField(max_length=100)
    apt_location = models.TextField(null=True)
    apt_area = models.IntegerField(null=True) # square feet
    apt_price = models.IntegerField(null=True) # in US dollars
    apt_beds = models.IntegerField(null=True)
    apt_baths = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    apt_lease = models.IntegerField(null=True) # months
    apt_deposit = models.IntegerField(null=True) # in US dollars
    apt_movein = models.DateField(null=True)
    def __str__(self):
        return self.apt_name

class Review(models.Model):
    apt_name = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    apt_reviewer = models.CharField(max_length=100)
    apt_review = models.TextField()
    # apt_stars = models.IntegerField(default=5)
    class Stars(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    apt_stars = models.IntegerField(choices=Stars.choices)

    def __str__(self):
        return "\"{}\" by \"{}\"".format(self.apt_name,self.apt_reviewer)
