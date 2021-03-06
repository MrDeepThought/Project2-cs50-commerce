# Generated by Django 2.2.2 on 2020-09-12 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200912_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AddField(
            model_name='listing',
            name='currentBid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='numBid',
            field=models.IntegerField(default=0),
        ),
    ]
