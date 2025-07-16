from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    house_number = models.PositiveIntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.house_number} {self.street}, {self.city}, {self.country}"
        
    class Meta:
        ordering = ["pk"]


class LocationCategories(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='category name')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["pk"]


class Location(models.Model):
    class Rating(models.IntegerChoices):
        NOCOMMENTS = 0
        POOR = 1
        NOTBAD = 2
        GOOD = 3
        VERYGOOD = 4
        EXELLENT = 5

    name = models.CharField(max_length=256, blank=False,  verbose_name='location name')
    description = models.TextField(max_length=512, blank=True, verbose_name='location description')
    rating = models.IntegerField(choices=Rating, default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='location address') 
    categories = models.ManyToManyField(LocationCategories, verbose_name='location categories')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='location owner')

    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) // len(reviews)

    def __str__(self):
        return f"{self.name} at" + str(self.address) + f" have rating of {self.rating}"

    class Meta:
        ordering = ["pk"]


class Review(models.Model):
    class Rating(models.IntegerChoices):
        POOR = 1
        NOTBAD = 2
        GOOD = 3
        VERYGOOD = 4
        EXELLENT = 5
    
    rating = models.IntegerField(choices=Rating)
    comment = models.TextField(max_length=512, verbose_name='review comment')
    likes = models.PositiveIntegerField(default=0, verbose_name='number of likes')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='number of dislikes')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='connected location')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='review author')

    def __str__(self):
        return f"Comment from {self.user} for {self.location.name}"

    class Meta:
        ordering = ["pk"]