# Generated by Django 2.2.2 on 2020-09-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200914_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='watchlists', to='auctions.Listing'),
        ),
    ]
