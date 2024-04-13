from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass 

class Category(models.Model):
    name = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.name
    
class Bid(models.Model):
    bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")
    def __str__(self):
        return f"{self.bid}"
    
    
class Auction_listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_owned")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist_User")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name="auctions")  

    def __str__(self):
        return f"{self.title} - Price: {self.price.bid}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    def __str__(self):
        return f"{self.commenter} comment on {self.auction}"