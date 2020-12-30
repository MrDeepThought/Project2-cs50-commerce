from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *

import datetime
watchCounter = 0

def index(request):
    global watchCounter

    if request.user.is_authenticated:
        try:
            watch = request.user.watchlist
        except ObjectDoesNotExist:
            watch = Watchlist(user=request.user)
            watch.save()
            print(f"{request.user} is associated with their watchlist!")

    activeListings = Listing.objects.filter(active=True).all()
    params = {
    "activeListings": activeListings,
    "watchCounter": watchCounter
    }
    return render(request, "auctions/index.html", params)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    global watchCounter
    watchCounter = 0
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, firstName=firstName, lastName=lastName)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateForm(forms.Form):
    categories = [(str(category),str(category))for category in Category.objects.all()]

    title = forms.CharField( max_length=64, min_length=1, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}), max_length=500)
    startBid = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))
    imageUrl = forms.URLField(required=False, widget=forms.URLInput(attrs={'class':'form-control'}))
    categories = forms.MultipleChoiceField(choices=categories, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control'}))


def create_listing(request,username):
    global watchCounter
    labels = ["Categories","Title", "Description", "Start Price", "Image URL"]

    form = CreateForm()
    form = zip(form,labels)
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startBid = form.cleaned_data["startBid"]
            imageUrl = form.cleaned_data["imageUrl"]
            if len(imageUrl) == 0:
                imageUrl = "https://dmhosiery.com/public/product_images/no_image.png"
            categories = form.cleaned_data["categories"]
            created = datetime.datetime.now()
            user = User.objects.get(username=username)
            currentBid = Bid(user=user, value=startBid)
            currentBid.save()

            listing = Listing(title=title, description=description, startBid=startBid, created=created,
            imageUrl=imageUrl, listingUser=user, active=True, currentBid=currentBid)
            listing.save()
            for name in categories:
                category = Category.objects.get(name=name)
                listing.categories.add(category)

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html", {
            "form": form,
            "watchCounter": watchCounter
            })

    return render(request, "auctions/create.html", {
    "form": form,
    "watchCounter": watchCounter
    })

@login_required()
def listing(request, username, listingId):
    global watchCounter

    listing = Listing.objects.get(id=listingId)
    categories = listing.categories.all()
    watchlist = request.user.watchlist
    watchlistListings = watchlist.listings.all()

    inWatchlist = listing in watchlistListings
    comments = listing.comments.all()

    params = {
    "listing": listing,
    "categories": categories,
    "WatchlistListings": watchlistListings,
    "watchCounter": watchCounter,
    "inWatchlist": inWatchlist,
    "comments": comments
    }

    if request.method == "POST":
        authUser = request.user
        value = request.POST['action']
        # add a bid if valid by the user
        if value == "bid":
            bidVal = request.POST['bidVal']
            if int(bidVal) > listing.currentBid.value:
                userBid = Bid(user=authUser,value=bidVal)
                userBid.save()
                listing.currentBid = userBid
                listing.numBid+=1
                listing.save()
                message = "success"
            else:
                message = "fail"

            params['message'] = message
            return render(request, "auctions/listing.html", params)

        # add the listing to the watchlist of the user
        elif value == "watchlist":
            watchlist.listings.add(listing)
            params['watchCounter']+=1
            watchCounter+=1

            return render(request, "auctions/listing.html", params)

        # close bid
        elif value == "close":
            listing.active = False
            listing.winnerUser = listing.currentBid.user
            listing.save()

            return render(request, "auctions/listing.html", params)

        # Comment on the listing
        else:
            description = request.POST['description']
            timestamp = datetime.datetime.now()
            author = request.user
            comment = Comment(author=author, description=description, timestamp=timestamp, listing=listing)
            comment.save()
            listing.comments.add(comment)
            params['comment'] = comment

            return render(request, "auctions/listing.html", params)

    return render(request, "auctions/listing.html", params)

def category_listings(request, categoryName):
    print(categoryName)
    category = Category.objects.get(name=categoryName)
    activeListings = category.listings.filter(active=True).all()
    params = {
    "activeListings": activeListings
    }

    return render(request, "auctions/index.html", params)

def categories_page(request):
    global watchCounter

    categories = Category.objects.all()
    print(categories)
    params = {
    "watchCounter": watchCounter,
    "categories": categories
    }
    return render(request, "auctions/categories.html", params)

def watchlist_page(request):
    global watchCounter
    watchCounter = 0
    watchlist = request.user.watchlist
    listings = watchlist.listings.all()

    params = {
    "watchCounter": watchCounter,
    "listings": listings
    }

    if request.method == "POST":
        listingId = request.POST["listingId"]
        listing = Listing.objects.get(id=listingId)
        watchlist.listings.remove(listing)
        listings = watchlist.listings.all()
        return render(request, "auctions/watchlist.html", params)

    return render(request, "auctions/watchlist.html", params)
