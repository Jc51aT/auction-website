# Generated by Django 3.0.8 on 2020-08-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auction_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_image',
            field=models.ImageField(default='static/auctions/images/default_img.png', null=True, upload_to='uploads/'),
        ),
        migrations.DeleteModel(
            name='Auction_Watchlist',
        ),
    ]
