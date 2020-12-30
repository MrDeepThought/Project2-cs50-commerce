from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    firstName = models.CharField(max_length=64, default="first name")
    lastName  = models.CharField(max_length=64, default="last name")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Category(models.Model):

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):

    user  = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    value = models.IntegerField(null = True)


class Listing(models.Model):

    title       = models.CharField(max_length=64)
    description = models.TextField(max_length=500, blank=True, null=True)
    startBid    = models.IntegerField()
    currentBid  = models.OneToOneField(Bid, on_delete=models.CASCADE, null=True, blank=True)
    imageUrl    = models.URLField(blank=True, null=True)
    categories  = models.ManyToManyField(Category, blank=True, related_name="listings")
    numBid      = models.IntegerField(default = 0)
    created     = models.DateTimeField(null=True, blank=True)
    listingUser = models.ForeignKey(User, related_name="createdListings", on_delete=models.CASCADE, null=True, blank=True)
    active      = models.BooleanField(default=False)
    winnerUser  = models.ForeignKey(User, related_name="achievedListings", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):

    author      = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    listing     = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=500)
    timestamp   = models.DateTimeField(null=True, blank=True)

class Watchlist(models.Model):

    user     = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    listings = models.ManyToManyField(Listing, related_name="watchlists", blank=True)
