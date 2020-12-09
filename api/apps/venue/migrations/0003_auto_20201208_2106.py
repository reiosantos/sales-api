# Generated by Django 3.1.4 on 2020-12-08 21:06

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('venue', '0002_auto_20201208_1822'),
	]

	operations = [
		migrations.AlterField(
			model_name='venuesetting',
			name='var_define',
			field=models.CharField(choices=[('dateFormat.shortTime', 'Time format (e.g. HH:mm)'), (
			'dateFormat.mediumDate', 'Date format (e.g. dd-MMM-yyy)'), ('dateFormat.medium',
																		'Date format with time (e.g. dd-MMM-yyyy HH:mm)'),
											('dateFormat.full',
											 'Date format with day-of-week and time (e.g. EEE d MMM HH:mm)'),
											('TERMS_URL', 'T&C link'),
											('PRIVACY_POLICY_URL', 'Privacy Policy link'), (
											'DEFAULT_LANGUAGE_CODE',
											'Default language (example: en-us)'), ('ENABLE_DEPOSIT',
																				   'Enable usage of the Deposit system for payments'),
											('DEFAULT_CURRENCY',
											 'Default currency for the Deposit system (example: usd, ush,...)'),
											('MANDATORY_CREDIT_CARD',
											 'User must enter their credit card info before accessing other resources'),
											('STARTING_DAY_IN_WEEK',
											 'Starting day in week for calendar, format: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday'),
											('VENUE_ADMIN_EMAIL', 'Venue Admin email'),
											('DEFAULT_SUPPORT_EMAIL', 'Venue Support Email'), (
											'SELLING_PRICE_BELOW_BUYING_PRICE',
											'Allow selling price to be less that buying price')],
								   max_length=100, null=True, unique=True),
		),
	]