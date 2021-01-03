# Generated by Django 3.1.4 on 2021-01-03 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
	dependencies = [
		('venue', '0004_auto_20201209_0010'),
		('inventory', '0002_auto_20210103_1035'),
	]

	operations = [
		migrations.AddField(
			model_name='itemtype',
			name='venue',
			field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
									related_name='items', to='venue.venue'),
			preserve_default=False,
		),
	]