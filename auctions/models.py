from django.contrib.auth.models import AbstractUser
from django.db import models


class Auction_Listing(models.Model):
    listing_price = models.IntegerField()
    listing_title = models.CharField(max_length=64)
    listing_description = models.CharField(max_length=256)
    listing_date = models.DateTimeField()
    listing_categories = models.CharField(max_length=128)
    listing_image = models.ImageField(null=True, upload_to='uploads/', default='auctions/static/auctions/images/default_img.png')
    listed_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.listing_title}"

    @property
    def get_listing_cat_num(self):
        return int(self.listing_categories)

class Auction_Bids(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    bid_date = models.DateTimeField('Bid date', auto_now_add=True)

    def __str__(self):
        return f"Bidder: {self.user.username}  Listing: {self.auction_listing}  Bid: {self.bid_amount}"

class Auction_Comments(models.Model):
    auction_listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    comment_date = models.DateTimeField('Comment date', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comments {self.comment} on {self.auction_listing}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction_Listing, blank=True, related_name="watchlist")

    def display_watchlist(self):
        return ', '.join(listing.listing_title for listing in self.watchlist.all()[:3])

    display_watchlist.short_description = 'Watchlist'




