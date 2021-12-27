# Generated by Django 3.1.4 on 2021-12-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('sales', '0004_itemsale_sold_length'),
	]

	operations = [
		migrations.AddField(
			model_name='itemsale',
			name='price_per_meter',
			field=models.DecimalField(blank=True, decimal_places=3,
									  help_text='Price per meter of wire sold', max_digits=13,
									  null=True),
		),
	]
