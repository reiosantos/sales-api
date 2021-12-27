# Generated by Django 3.1.4 on 2021-12-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('inventory', '0005_auto_20211110_1506'),
	]

	operations = [
		migrations.AddField(
			model_name='itemtype',
			name='available_length',
			field=models.DecimalField(blank=True, decimal_places=3,
									  help_text='New Length of wire in metres', max_digits=13,
									  null=True),
		),
		migrations.AddField(
			model_name='itemtype',
			name='color',
			field=models.CharField(blank=True, max_length=200, null=True),
		),
		migrations.AddField(
			model_name='itemtype',
			name='is_available',
			field=models.BooleanField(default=True, null=True),
		),
		migrations.AddField(
			model_name='itemtype',
			name='is_wire_type',
			field=models.BooleanField(default=False, null=True),
		),
		migrations.AddField(
			model_name='itemtype',
			name='latest_length',
			field=models.DecimalField(blank=True, decimal_places=3,
									  help_text='New Length of wire in metres', max_digits=13,
									  null=True),
		),
		migrations.AddField(
			model_name='itemtype',
			name='total_length',
			field=models.DecimalField(blank=True, decimal_places=3,
									  help_text='Length of wire in metres', max_digits=13,
									  null=True),
		),
	]