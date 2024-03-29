# Generated by Django 3.1.4 on 2021-01-03 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
	initial = True

	dependencies = [
		('customers', '0001_initial'),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
		('inventory', '0003_itemtype_venue'),
	]

	operations = [
		migrations.CreateModel(
			name='ItemSale',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
										verbose_name='ID')),
				('created_at', models.DateTimeField(auto_now_add=True, null=True)),
				('modified_at', models.DateTimeField(auto_now=True, null=True)),
				('unit_price', models.DecimalField(decimal_places=3, default=0, max_digits=13)),
				('quantity', models.IntegerField(default=1)),
				('customer',
				 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
								   to='customers.customer')),
				('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
										   to='inventory.itemtype')),
				('sold_by',
				 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
								   to=settings.AUTH_USER_MODEL)),
			],
			options={
				'abstract': False,
			},
		),
	]
