# Generated by Django 3.1.4 on 2020-12-08 22:54

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		('venue', '0003_auto_20201208_2106'),
		('user', '0004_auto_20201208_1822'),
	]

	operations = [
		migrations.RenameField(
			model_name='venueviewertype',
			old_name='name',
			new_name='role',
		),
		migrations.AlterUniqueTogether(
			name='venueviewertype',
			unique_together={('venue', 'role')},
		),
	]
