from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from .models import Auction_listing
from .models import Category
from .models import Bid
from .models import Comment
from  django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    activeListings = Auction_listing.objects.filter(active = True)
    return render(request, "auctions/index.html",{
                    "items" :activeListings
                
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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
    
    
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url")
        price = request.POST.get("price")
        category_name = request.POST.get("category")
        owner = request.user

        if title and description and image_url and price and category_name:
            try:
                price = float(price)
            except ValueError:
                return render(request, "auctions/error.html", {'message': "Invalid price. Please enter a valid number."})

            owner = User.objects.get(username=owner)
            category = Category.objects.get(name=category_name)
            bid = Bid.objects.create(bid=price, bidder=owner)

            new_listing = Auction_listing.objects.create(
                title=title,
                description=description,
                image_url=image_url,
                price=bid,
                category=category,
                owner=owner
            )
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/error.html", {'message': "Please fill out all the required fields."})
    else:
        return render(request, "auctions/create.html", {
            "users": User.objects.all(),
            "categorys": Category.objects.all()
        })

def watchlist(request):
    cUser = request.user
    watchlist_items = cUser.watchlist_User.filter()
    return render(request, "auctions/watchlist.html", {
        "items": watchlist_items
    })

def categorys(request):
    return render(request, "auctions/categorys.html", {
        "categorys" :Category.objects.all()
        })

    

def listing(request, id): 
    list = Auction_listing.objects.filter(id=id).first()
    if list is not None:
        isinWL = request.user in list.watchlist.all()
        allcomments = Comment.objects.filter(auction=list)
        listac = list.active
        cUser = request.user
        owner = list.owner
        winner = list.price.bidder
        print(winner)
        return render(request, "auctions/listing.html",{
            "items": list,
            "isinWL": isinWL,
            "cUser": cUser,
            "owner": owner,
            "allcomments": allcomments,
            "listac": listac,
            "winner":winner
        })
    else:
        return render(request, "auctions/error.html", {'message': "Item not found"})
    
def addwatchlist(request,id):
    list = Auction_listing.objects.filter(active=True, id=id).first()
    cUser = request.user
    list.watchlist.add(cUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def removewatchlist(request,id):
    list = Auction_listing.objects.filter(active=True, id=id).first()
    cUser = request.user
    list.watchlist.remove(cUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


from django.shortcuts import render

def showCategory(request):
    if request.method == "POST":
        category_name = request.POST.get("category")
        activeListings = Auction_listing.objects.filter(active=True, category__name=category_name)
        allcategories = Category.objects.all() 
        return render(request, "auctions/index.html", {
            "items": activeListings,
            "categorys": allcategories
        })
    else:
        return render(request, "auctions/error.html", {'message': "Not valid method"})

        
def comment(request, id):
    if request.method == 'POST':
        cUser = request.user
        listing = Auction_listing.objects.get(pk=id)

        if 'comment' in request.POST and request.POST['comment']:
            msg = request.POST['comment']

            new_comment = Comment.objects.create(
                commenter=cUser,
                auction=listing,
                comment=msg
            )
            return HttpResponseRedirect(reverse("listing", args=(id, )))
        else:
            return render(request, "auctions/error.html", {'message': "Please enter a non-empty comment."})
    else:

        return HttpResponseRedirect(reverse("listing", args=(id, )))



def bid(request, id):
    if request.method == 'POST':
        cUser = request.user
        listing = Auction_listing.objects.get(pk=id)

        if any(request.POST.values()):
            if 'price' in request.POST and request.POST['price']:
                try:
                    bid_price = float(request.POST['price'])
                except ValueError:
                    return render(request, "auctions/error.html", {'message': "Invalid bid value. Please enter a valid number."})

                if not listing.price or listing.price.bid < bid_price:
                    new_bid = Bid.objects.create(
                        bid=bid_price,
                        bidder=cUser
                    )
                    listing.price = new_bid
                    listing.save()
                    return HttpResponseRedirect(reverse("listing", args=(id, )))
                else:
                    return render(request, "auctions/error.html", {'message': "Your bid must be higher than the current highest bid."})
            else:
                return render(request, "auctions/error.html", {'message': "Please enter a valid bid."})
        else:
            return render(request, "auctions/error.html", {'message': "Please fill out the form before submitting."})
    else:

        return HttpResponseRedirect(reverse("listing", args=(id, )))
        
        
def closeAuc(request, id):
    if request.method == 'POST':
        list = Auction_listing.objects.get(pk=id)
        isinWL = request.user in list.watchlist.all()
        allcomments = Comment.objects.filter(auction=list)
        listac = list.active
        list.active = False
        cUser = request.user
        owner = list.owner
        winner = list.price.bidder
        print(winner)
        list.save()   
        return render(request, "auctions/listing.html",{
            "items": list,
            "isinWL": isinWL,
            "cUser": cUser,
            "owner": owner,
            "allcomments": allcomments,
            "listac": listac,
            "winner": winner
        })
    else:
        return render(request, "auctions/error.html", {'message': "Method no valid. If you wanna see the item use /listing/'item id'"})
        
