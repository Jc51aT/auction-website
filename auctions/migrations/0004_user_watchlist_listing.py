# Generated by Django 3.0.8 on 2020-08-10 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200807_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist_listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auctions.Auction_Listing'),
        ),
    ]