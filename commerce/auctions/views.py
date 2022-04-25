from email.mime import image
import os
import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from commerce.settings import BASE_DIR

from .models import *


class ProductForm(forms.Form):
    title = forms.CharField(label="Name of product", max_length=64, widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}))
    desc = forms.CharField(label="Description of product", max_length=64, widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}))
    price = forms.CharField(label="Minimum bid", max_length=6, widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}))
    
    category = forms.CharField(label="Category (Optional)", max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}), required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "lists": List.objects.filter(closed=False)
    })


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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Creating an item
def create(request):
    if request.method == "POST":
        item = request.POST["title"]
        description = request.POST["desc"]
        start = int(request.POST["price"])
        img = request.FILES.get('photo') 
        imgname = request.FILES.get('photo').name
        itemType = request.POST["category"]
        if itemType is not None :
            product = List(
                title=item, 
                desc=description, 
                price=start, 
                image=img, 
                imguser=imgname,
                category=itemType,
                owner=User.objects.get(username=request.user),
                closed=False)
            product.save()
            return HttpResponseRedirect(reverse("index"))
        elif itemType is None:
            product = List(
                title=item, 
                desc=description, 
                image=img,
                imguser=imgname,
                category=None,
                owner=User.objects.get(username=request.user),
                closed=False)
            product.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/create.html", {
            "form": ProductForm(),
            "message": "Please fill out all the detail"
        })
    else:
        return render(request, "auctions/create.html", {
            "form": ProductForm()
        })

# Render the listing page
def listing(request, listing_item):
    item = List.objects.get(id=listing_item)
    if request.method == "GET":
        seller = List.objects.get(id=listing_item).owner
        # auction = List.objects.get(id=listing_item)
        comment = item.comments.all()
        return render(request, 'auctions/auction.html', {
            'auction': item,
            'person': seller,
            'comment': comment,
            'bids': item.price,
        })
        
# Allow the user to bid
def bid(request, listing_item):
    if request.method == "POST":
        item = List.objects.get(id=listing_item)
        maxBid = request.POST["maxBid"]
        if request.user.id is None:
            return HttpResponseRedirect(reverse("login"))
        if maxBid is None:
            return HttpResponse('Please make a valid bid')
        bid = Bids.objects.create(user=request.user, auction=item, cost=maxBid)
        
        # Accept the bid if it's higher than the last bid or initual price if it's the first bid
        if item.bids is None:
            item.bids = bid
            item.save()
        elif item.bids.cost < int(bid.cost):
            item.bids = bid
            item.save()
        else:
            return HttpResponse('Your bid must be higher than the current bid')
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse('Please enter a valid bid')

# Close the item and declare the winner of that item
def close(request, listing_item):
    if request.method == "POST":
        item = List.objects.get(id=listing_item)
        item.closed = True
        item.save()
        if item.bids:
            return HttpResponse(f'{item.bids.user} is the winner of this item')
        else:
            return HttpResponseRedirect(reverse("index"))

# Put the item in the watchlist
def watch(request, listing_item):
    if request.method == "POST":
        item = List.objects.get(id=listing_item)
        if request.user.id is None:
            return HttpResponseRedirect(reverse("login"))
        try:
            watch = WatchList.objects.get(watch_user=request.user)
        except:
            watch = WatchList(watch_user=request.user)
            watch.save()

        # Add if item is not in watchlist and remove if already is in the watchlist
        if item in watch.auctions.all():
            watch.auctions.remove(item)
            watch.save() 
        else:
            watch.auctions.add(item)
            watch.save() 
        return HttpResponseRedirect(reverse("index"))

# Render watchlist page
def watch_open(request):
    #watch = get_object_or_404(WatchList, watch_user=request.user)
    try:
        myWatchList = WatchList.objects.get(watch_user=request.user)
    except WatchList.DoesNotExist:
        return render(request, "auctions/watchlistnotfound.html")
    return render(request, "auctions/watchlist.html", {
        'watchList': myWatchList.auctions.filter(closed=False)
    })

# Allow the user to comment
def add_comment(request, listing_item):
    if request.method == "POST":
        item = List.objects.get(id=listing_item)
        comment_input = request.POST["comment"]
        comment_object = Comment.objects.create(comment_user=request.user, commentInput=comment_input) 
        item.comments.add(comment_object)
        if request.user.id is None:
            return HttpResponseRedirect(reverse("login"))
        return HttpResponseRedirect(reverse("index")) 

# Render category page
def category(request):
    if request.method == "POST":
        category_input = request.POST["category"]
        return render(request, "auctions/category.html", {
        "lists": List.objects.filter(category=category_input, closed=False)
    })
    else:
        return render(request, "auctions/category.html", {
        "lists": List.objects.filter(closed=False)
    })