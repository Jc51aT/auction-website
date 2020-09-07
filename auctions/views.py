from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction_Bids, Auction_Comments, Auction_Listing
from .forms import *
from django.utils import timezone,dateformat

def index(request):
    return render(request, "auctions/index.html",{
        "Auction_Listings": Auction_Listing.objects.all(),
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

@login_required
def create_listing(request):
    listing = Auction_Listing()

    if request.method == "POST":

        form = CreateListingForm(request.POST, request.FILES)

        if form.is_valid():
            
            listing.listing_title = form.cleaned_data["listing_title"]
            listing.listing_price = int(form.cleaned_data["listing_price"])
            listing.listing_description = form.cleaned_data["listing_description"]
            listing.listing_categories = form.cleaned_data["listing_categories"]
            listing.listing_date = timezone.now()
            print(form.cleaned_data["listing_image"])
            if form.cleaned_data["listing_image"]:
                listing.listing_image = form.cleaned_data["listing_image"]
            else:
                listing.listing_image = None
            listing.listed_by = request.user

            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {"form":form})

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "User": request.user,
        "watchlist": request.user.watchlist.all(),
    })

@login_required
def categories(request):
    listing_categories_present = set(Auction_Listing.objects.values_list("listing_categories", flat=True))
    
    return render(request, "auctions/categories.html",{
        "Auction_Listings": Auction_Listing.objects.all(),
        "listing_cats": listing_categories_present,
    })

@login_required
def category(request, listing_categories):
    listings = Auction_Listing.objects.filter(listing_categories=listing_categories)
    return render(request, "auctions/category.html",{
        "Auction_Listings": listings,
        "category": listings[0].listing_categories
    })


def auction(request, listing_id):
    listing = Auction_Listing.objects.get(id=listing_id)
    max_bid = Auction_Bids.objects.filter(auction_listing=listing).order_by('bid_amount').first()
    watchlist =  request.user.watchlist.all()
    current_user_name = request.user.username
    listing_comments = Auction_Comments.objects.filter(auction_listing=listing)

    if request.method == "POST":
        bid = request.POST["bid"]

        if bid:
            return render(request, "auctions/auction.html", {
                "listing": listing,
                "max_user": max_bid.user if max_bid else None,
                "watchlist": watchlist,
                "comments": listing_comments,
                "user_name": current_user_name,
                "num_bids": len(Auction_Bids.objects.filter(auction_listing=listing)),
                "message": None
            })
            
        elif int(bid) > listing.listing_price:
            listing.listing_price = bid
            listing.save()
            auction_bid = Auction_Bids()
            auction_bid.bid_amount = bid
            auction_bid.user = request.user
            auction_bid.auction_listing = listing
            auction_bid.save()

        else:
            return render(request, "auctions/auction.html", {
                "listing": listing,
                "max_user": max_bid.user if max_bid else None,
                "comments": listing_comments,
                "user_name": current_user_name,
                "watchlist": watchlist,
                "num_bids": len(Auction_Bids.objects.filter(auction_listing=listing)),
                "message": "Bid must be great then current price."
            })
            
    return render(request, "auctions/auction.html", {
        "listing": listing,
        "max_user": max_bid.user if max_bid else None,
        "user_name": current_user_name,
        "comments": listing_comments,
        "watchlist": watchlist,
        "num_bids": len(Auction_Bids.objects.filter(auction_listing=listing))
    })

def watchlist_ajax(request,listing_id):
    u = request.user
    listing = Auction_Listing.objects.get(id=listing_id)
    data = {'success': False}

    if request.method=='POST':
        u.watchlist.add(listing)
        u.save()
        data['success'] = True
    return JsonResponse(data)

def watchlist_remove_ajax(request,listing_id):
    u = request.user
    listing = Auction_Listing.objects.get(id=listing_id)
    data = {'success': False}

    if request.method=='POST':
        u.watchlist.remove(listing)
        u.save()
        data['success'] = True
    return JsonResponse(data)

def comment_ajax(request,listing_id):
    user = request.user
    user_name = user.username
    listing = Auction_Listing.objects.get(id=listing_id)
    comment = request.POST.get('comment',None)

    data = {
            'success': False,
            'user_name': user_name,
            'current_date': dateformat.format(timezone.now(), 'Y-m-d H:i:s')
            }
    if request.method=='POST' and comment != '':
        auction_comm = Auction_Comments()
        auction_comm.user = user
        auction_comm.comment = comment
        auction_comm.auction_listing = listing
        auction_comm.save()
        data['success'] = True
    return JsonResponse(data)

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
