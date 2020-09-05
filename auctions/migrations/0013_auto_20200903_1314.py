# Generated by Django 3.0.8 on 2020-09-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200831_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_comments',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Comment date'),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_image',
            field=models.ImageField(default='auctions/static/auctions/images/default_img.png', null=True, upload_to='uploads/'),
        ),
    ]