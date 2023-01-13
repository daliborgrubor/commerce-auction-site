from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def index(request):
    active_listings = Listing.objects.filter(is_active = True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : active_listings,
        "categories" : all_categories
    })

def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    is_in_watchlist = request.user in listing_data.watchlist.all()
    is_owner = request.user.username == listing_data.owner.username
    all_comments = Comment.objects.filter(listing=listing_data)
    return render(request, "auctions/listing.html", {
        "listing" : listing_data,
        "is_in_watchlist" : is_in_watchlist,
        "is_owner" : is_owner,
        "all_comments" : all_comments
    })

def add_bid(request, id):
    new_bid = request.POST.get('new_bid')
    listing_data = Listing.objects.get(pk=id)
    if int(new_bid) > listing_data.price.bid:
        new_price = Bid(user=request.user, bid=int(new_bid))
        new_price.save()
        listing_data.price = new_price
        listing_data.save()
        return render (request, "auctions/listing.html", {
            "listing" : listing_data,
            "message" : "Bid updated successfully!",
            "update" : True
        })
    else:
        return render (request, "auctions/listing.html", {
            "listing" : listing_data,
            "message" : "Bid update failed!",
            "update" : False
        })

def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.is_active = False
    listing_data.save()
    is_in_watchlist = request.user in listing_data.watchlist.all()
    is_owner = request.user.username == listing_data.owner.username
    all_comments = Comment.objects.filter(listing=listing_data)
    return render(request, "auctions/listing.html", {
        "listing" : listing_data,
        "is_in_watchlist" : is_in_watchlist,
        "is_owner" : is_owner,
        "update" : True,
        "message" : "Auction is closed!",
        "all_comments" : all_comments
    })

def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    comment_message = request.POST['new_comment']
    new_comment = Comment(
        author = current_user,
        listing = listing_data,
        comment_message = comment_message
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    current_user = request.user
    listings = current_user.listing_to_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def remove_from_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def add_to_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def display_by_category(request):
    if request.method == "POST":
        category_from_form = request.POST["category"]
        category = Category.objects.get(category_name = category_from_form)
        active_listings = Listing.objects.filter(is_active = True, category = category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings" : active_listings,
            "categories" : all_categories
        })

def create_listing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories" : all_categories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        category = request.POST.get("category")
        description = request.POST["description"]
        img_url = request.POST["img_url"]
        price = request.POST["price"]
        # Who enters data
        current_user = request.user
        # Get all content for category
        category_data = Category.objects.get(category_name = category)
        # Create a bid object
        bid = Bid(bid=int(price), user=current_user)
        bid.save()
        # Create object and save to database
        new_listing = Listing(
            title = title, 
            category = category_data,
            description = description,
            img_url = img_url,
            price = bid,
            owner = current_user
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))

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
