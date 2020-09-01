from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Auction_Listing, Auction_Bids, Auction_Comments

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction_Listing)
admin.site.register(Auction_Bids)
admin.site.register(Auction_Comments)