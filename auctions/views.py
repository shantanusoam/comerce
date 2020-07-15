from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bids, Comment, wishlist
from django import forms


def index(request):
    return render(request, "auctions/index.html",{
                "check": Listing.objects.all(),
                "bids": Bids.objects.all()
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

class create_form(forms.Form):
    CATEGORIES = (
        ("None", "None"),
        ("Gadget", "Gadget"),
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home")
        )
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", max_length=200, widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="Enter starting bid")
    image_path = forms.CharField(label="Image Path")
    category = forms.ChoiceField(label="Category", choices=CATEGORIES)


class place_bid(forms.Form):
    bid = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter your bid here'}))

class comment_form(forms.Form):
    comment = forms.CharField(label="", max_length=100, widget=forms.Textarea)

@login_required
def create_list(request):
    if request.method == "POST":
        form = create_form(request.POST)
        if form.is_valid():
            user = request.user
            title = request.POST.get("title")
            desc = request.POST.get("description")
            bid = request.POST.get("starting_bid")
            image = request.POST.get("image_path")
            categ = request.POST.get("category")
            s = Listing(title=title, description=desc, starting_bid=bid, image_path=image, category=categ, bidding_user=user)
            s.save()
            listing_object = Listing.objects.get(title=title)
            b = Bids(user=user, auction=listing_object, bid=bid)
            b.save()
            return HttpResponseRedirect(reverse("index"))



    check = Listing.objects.all()
    return render(request, "auctions/create_list.html",{
        "form": create_form()
        })

@login_required
def description(request, title):
    desc = Listing.objects.get(title=title)
    if request.method == "POST":
        form = place_bid(request.POST)
        if form.is_valid():
            bid = request.POST.get("bid")
            bid_model = Bids.objects.get(auction=desc.id)
            if int(bid_model.bid) < int(bid):
                bid_model.user = request.user
                bid_model.auction = Listing.objects.get(title=title)
                bid_model.bid = bid
            else:
                desc = Listing.objects.get(title=title)
                bid = Bids.objects.get(auction=desc.id)
                comment = Comment.objects.all()
                return render(request, "auctions/description.html",{
                    "desc": desc,
                    "bid": bid,
                    "form": place_bid(),
                    "message": "Placed bid should be greater than existing one",
                    "comment": comment_form(),
                    "comments": comment
                    }) 

            bid_model.save()

        commentform = comment_form(request.POST)
        if commentform.is_valid():
            comment = request.POST.get("comment")
            user = request.user
            auction = Listing.objects.get(title=title)
            c = Comment(user=user, auction=auction, comment=comment)
            c.save()
            #return HttpResponseRedirect(reverse("description", kwargs={'title': title}))

    desc = Listing.objects.get(title=title)
    bid = Bids.objects.get(auction=desc.id)
    comment = Comment.objects.all()
    return render(request, "auctions/description.html",{
        "desc": desc,
        "bid": bid,
        "form": place_bid(),
        "comment": comment_form(),
        "comments": comment
        }) 

@login_required
def addwishlist(request, title):
    user = request.user
    auction = Listing.objects.get(title=title)
    w = wishlist(user = user , auction = auction)
    w.save()
    return HttpResponseRedirect(reverse("description"))