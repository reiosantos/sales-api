# Generated by Django 3.1.4 on 2021-11-10 15:06

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20211110_1506'),
        ('venue', '0004_auto_20201209_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertype',
            name='venues',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='venues',
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='users',
            field=models.ManyToManyField(related_name='venues', through='venue.UsersVenues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='venuesetting',
            name='var_define',
            field=models.CharField(choices=[('dateFormat.shortTime', 'Time format (e.g. HH:mm)'), ('dateFormat.mediumDate', 'Date format (e.g. dd-MMM-yyy)'), ('dateFormat.medium', 'Date format with time (e.g. dd-MMM-yyyy HH:mm)'), ('dateFormat.full', 'Date format with day-of-week and time (e.g. EEE d MMM HH:mm)'), ('TERMS_URL', 'T&C link'), ('PRIVACY_POLICY_URL', 'Privacy Policy link'), ('DEFAULT_LANGUAGE_CODE', 'Default language (example: en-us)'), ('ENABLE_DEPOSIT', 'Enable usage of the Deposit system for payments'), ('DEFAULT_CURRENCY', 'Default currency for the Deposit system (example: usd, ush,...)'), ('MANDATORY_CREDIT_CARD', 'User must enter their credit card info before accessing other resources'), ('STARTING_DAY_IN_WEEK', 'Starting day in week for calendar, format: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday'), ('VENUE_ADMIN_EMAIL', 'Venue Admin email'), ('DEFAULT_SUPPORT_EMAIL', 'Venue Support Email'), ('ALLOW_SELLING_PRICE_BELOW_BUYING_PRICE', 'Allow selling price to be less than buying price')], max_length=100, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
    ]
